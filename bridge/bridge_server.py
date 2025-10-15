#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP服务器 - Chrome扩展桥接通信
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
try:
    from http.server import ThreadingHTTPServer as _ThreadingHTTPServer
except ImportError:
    from socketserver import ThreadingMixIn
    class _ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True


class BridgeRequestHandler(BaseHTTPRequestHandler):
    """Bridge请求处理器"""
    
    def __init__(self, *args, account_manager=None, on_account_added=None, **kwargs):
        self.account_manager = account_manager
        self.on_account_added = on_account_added
        super().__init__(*args, **kwargs)
    
    def _set_cors_headers(self):
        """设置CORS头部"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Extension-ID')
    
    def _send_json_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        response_data = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response_data.encode('utf-8'))
    
    def _verify_extension(self):
        """验证请求来自我们的扩展"""
        extension_id = self.headers.get('X-Extension-ID')
        return extension_id == 'warp-account-bridge-v1'
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/health':
            self._send_json_response(200, {
                'status': 'ok',
                'service': 'warp-bridge',
                'timestamp': int(time.time())
            })
        else:
            self._send_json_response(404, {'error': 'Endpoint not found'})
    
    def do_POST(self):
        """处理POST请求"""
        if not self._verify_extension():
            self._send_json_response(403, {'error': 'Unauthorized - Invalid extension ID'})
            return
        
        if self.path == '/add-account':
            self._handle_add_account()
        elif self.path == '/setup-bridge':
            self._handle_setup_bridge()
        else:
            self._send_json_response(404, {'error': 'Endpoint not found'})
    
    def _handle_add_account(self):
        """处理从扩展添加账号"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_json_response(400, {'error': 'Empty request body'})
                return
            
            body = self.rfile.read(content_length)
            account_data = json.loads(body.decode('utf-8'))
            
            # 验证账号数据结构
            if not self._validate_account_data(account_data):
                self._send_json_response(400, {'error': 'Invalid account data structure'})
                return
            
            # 转换为JSON字符串
            account_json = json.dumps(account_data, ensure_ascii=False)
            
            # 使用AccountManager添加账号
            if self.account_manager:
                success, message = self.account_manager.add_account(account_json)
                
                if success:
                    print(f"✅ Bridge: 账号已添加 - {account_data.get('email', 'Unknown')}")
                    
                    self._send_json_response(200, {
                        'success': True,
                        'message': message,
                        'email': account_data.get('email')
                    })
                    
                    # 在后台触发UI刷新
                    if self.on_account_added:
                        try:
                            threading.Thread(
                                target=self.on_account_added,
                                args=(account_data.get('email'),),
                                daemon=True
                            ).start()
                        except Exception as e:
                            print(f"⚠️  UI刷新错误: {e}")
                    return
                else:
                    print(f"❌ Bridge: 账号添加错误 - {message}")
                    self._send_json_response(400, {
                        'success': False,
                        'error': message
                    })
            else:
                self._send_json_response(500, {'error': 'Account manager not available'})
        
        except json.JSONDecodeError:
            self._send_json_response(400, {'error': 'Invalid JSON data'})
        except Exception as e:
            print(f"❌ Bridge: 添加账号错误 - {str(e)}")
            self._send_json_response(500, {'error': f'Server error: {str(e)}'})
    
    def _handle_setup_bridge(self):
        """处理Bridge设置"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                setup_data = json.loads(body.decode('utf-8'))
                print(f"🔗 Bridge: 扩展已连接 - ID: {setup_data.get('extensionId', 'Unknown')}")
            
            self._send_json_response(200, {
                'success': True,
                'message': 'Bridge setup successful',
                'server_version': '1.0'
            })
        
        except Exception as e:
            print(f"❌ Bridge: 设置错误 - {str(e)}")
            self._send_json_response(500, {'error': f'Setup error: {str(e)}'})
    
    def _validate_account_data(self, data):
        """验证账号数据结构"""
        try:
            required_fields = ['email', 'stsTokenManager']
            for field in required_fields:
                if field not in data:
                    return False
            
            sts_manager = data['stsTokenManager']
            required_sts_fields = ['accessToken', 'refreshToken']
            for field in required_sts_fields:
                if field not in sts_manager:
                    return False
            
            return True
        except Exception:
            return False
    
    def log_message(self, format, *args):
        """静默日志记录"""
        pass


class WarpBridgeServer:
    """Warp Bridge HTTP服务器"""
    
    def __init__(self, account_manager, port=8765, on_account_added=None):
        self.account_manager = account_manager
        self.port = port
        self.server = None
        self.server_thread = None
        self.running = False
        self.on_account_added = on_account_added
    
    def start(self):
        """启动Bridge服务器"""
        try:
            if self.running:
                print("⚠️  Bridge服务器已在运行")
                return True
            
            def handler(*args, **kwargs):
                return BridgeRequestHandler(
                    *args,
                    account_manager=self.account_manager,
                    on_account_added=self.on_account_added,
                    **kwargs
                )
            
            self.server = _ThreadingHTTPServer(('127.0.0.1', self.port), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            self.running = True
            
            print(f"✅ Bridge服务器已启动 - http://127.0.0.1:{self.port}")
            return True
        
        except OSError as e:
            if 'address already in use' in str(e).lower():
                print(f"❌ 端口{self.port}已被占用")
            else:
                print(f"❌ Bridge服务器启动错误: {e}")
            return False
        except Exception as e:
            print(f"❌ Bridge服务器启动错误: {e}")
            return False
    
    def stop(self):
        """停止Bridge服务器"""
        try:
            if self.server and self.running:
                self.server.shutdown()
                self.server.server_close()
                self.running = False
                print("✅ Bridge服务器已停止")
                return True
            return False
        except Exception as e:
            print(f"❌ Bridge服务器停止错误: {e}")
            return False
    
    def is_running(self):
        """检查服务器是否运行"""
        return self.running and self.server_thread and self.server_thread.is_alive()

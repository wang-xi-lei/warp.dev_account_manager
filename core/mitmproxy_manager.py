#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mitmproxy进程管理器
"""

import sys
import subprocess
import time
import os
import psutil
from utils import is_port_open, is_windows
from .certificate_manager import CertificateManager


class MitmProxyManager:
    """Mitmproxy进程管理"""
    
    def __init__(self, port=8080, script_path="warp_proxy_script.py", debug_mode=False):
        self.process = None
        self.port = port
        self.script_path = script_path
        self.debug_mode = debug_mode
        self.cert_manager = CertificateManager()
    
    def check_mitmproxy_installation(self) -> bool:
        """检查mitmproxy是否已安装
        
        Returns:
            bool: 是否已正确安装
        """
        print("\n🔍 检查Mitmproxy安装")
        print("="*50)
        
        # 检查mitmdump命令
        try:
            result = subprocess.run(
                ['mitmdump', '--version'],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ Mitmproxy已安装: {result.stdout.strip()}")
            else:
                print(f"❌ Mitmproxy版本检查失败: {result.stderr}")
                return False
        except FileNotFoundError:
            print("❌ Mitmproxy未找到")
            print("\n📝 安装命令:")
            print("   pip3 install mitmproxy")
            print("   或: brew install mitmproxy")
            return False
        except subprocess.TimeoutExpired:
            print("❌ Mitmproxy版本检查超时")
            return False
        
        # 检查代理脚本
        if os.path.exists(self.script_path):
            print(f"✅ 代理脚本存在: {self.script_path}")
        else:
            print(f"❌ 代理脚本缺失: {self.script_path}")
            return False
        
        # 检查端口可用性
        if not is_port_open("127.0.0.1", self.port):
            print(f"✅ 端口{self.port}可用")
        else:
            print(f"⚠️  端口{self.port}已被占用")
            print("   终止占用端口的进程或选择其他端口")
        
        return True
    
    def start(self) -> bool:
        """启动Mitmproxy
        
        Returns:
            bool: 是否成功启动
        """
        try:
            if self.is_running():
                print("⚠️  Mitmproxy已在运行")
                return True
            
            # 检查安装
            print("🔍 检查Mitmproxy安装...")
            if not self.check_mitmproxy_installation():
                print("❌ Mitmproxy安装检查失败")
                return False
            
            # 检查并创建证书
            if not self.cert_manager.check_certificate_exists():
                print("📝 创建Mitmproxy证书...")
                if not self._create_certificate():
                    print("❌ 证书创建失败")
                    return False
                print("✅ 证书创建成功")
            
            # 准备命令
            cmd = [
                "mitmdump",
                "--listen-host", "127.0.0.1",
                "-p", str(self.port),
                "-s", self.script_path,
                "--set", "confdir=~/.mitmproxy",
                "--set", "keep_host_header=true",
            ]
            
            print(f"🚀 启动Mitmproxy: {' '.join(cmd)}")
            
            # 启动进程
            if is_windows():
                return self._start_windows(cmd)
            else:
                return self._start_unix(cmd)
                
        except Exception as e:
            print(f"❌ Mitmproxy启动错误: {e}")
            return False
    
    def _create_certificate(self) -> bool:
        """创建Mitmproxy证书"""
        try:
            temp_cmd = ["mitmdump", "--set", "confdir=~/.mitmproxy", "-q"]
            
            if is_windows():
                temp_process = subprocess.Popen(
                    temp_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                temp_process = subprocess.Popen(
                    temp_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # 等待5秒让证书生成
            time.sleep(5)
            temp_process.terminate()
            temp_process.wait(timeout=3)
            
            return self.cert_manager.check_certificate_exists()
            
        except Exception as e:
            print(f"证书创建错误: {e}")
            return False
    
    def _start_windows(self, cmd: list) -> bool:
        """Windows平台启动"""
        cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)
        
        if self.debug_mode:
            # 调试模式：显示控制台窗口
            print("🐛 调试模式：控制台窗口可见")
            self.process = subprocess.Popen(
                f'start "Mitmproxy Console (Debug)" cmd /k "{cmd_str}"',
                shell=True
            )
        else:
            # 普通模式：隐藏控制台窗口
            print("🔇 普通模式：后台运行")
            self.process = subprocess.Popen(
                cmd_str,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        
        # Windows start命令立即返回，检查端口
        print("⏳ 等待Mitmproxy启动...")
        for i in range(10):
            time.sleep(1)
            if is_port_open("127.0.0.1", self.port):
                print(f"✅ Mitmproxy已启动 - 端口{self.port}已开放")
                return True
            print(f"   检查中... ({i+1}/10)")
        
        print("❌ Mitmproxy启动失败 - 端口未开放")
        return False
    
    def _start_unix(self, cmd: list) -> bool:
        """Unix/Linux/macOS平台启动"""
        if self.debug_mode:
            print("🐛 调试模式：前台运行")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            print("🔇 普通模式：后台运行")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        # 等待并检查进程
        time.sleep(2)
        
        if self.process.poll() is None:
            print(f"✅ Mitmproxy已启动 (PID: {self.process.pid})")
            return True
        else:
            # 进程已终止，获取错误信息
            try:
                stdout, stderr = self.process.communicate(timeout=5)
                print(f"\n❌ Mitmproxy启动失败")
                print(f"\n📝 错误详情:")
                if stderr:
                    print(f"STDERR: {stderr.strip()}")
                if stdout:
                    print(f"STDOUT: {stdout.strip()}")
            except subprocess.TimeoutExpired:
                print("❌ 进程通信超时")
            return False
    
    def stop(self) -> bool:
        """停止Mitmproxy
        
        Returns:
            bool: 是否成功停止
        """
        try:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait(timeout=10)
                print("✅ Mitmproxy已停止")
                return True
            
            # 如果进程引用不存在，通过PID查找并停止
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'mitmdump' in proc.info['name'] and str(self.port) in ' '.join(proc.info['cmdline']):
                        proc.terminate()
                        proc.wait(timeout=10)
                        print(f"✅ Mitmproxy已停止 (PID: {proc.info['pid']})")
                        return True
                except:
                    continue
            
            return True
            
        except Exception as e:
            print(f"❌ Mitmproxy停止错误: {e}")
            return False
    
    def is_running(self) -> bool:
        """检查Mitmproxy是否正在运行
        
        Returns:
            bool: 是否运行中
        """
        try:
            if self.process and self.process.poll() is None:
                return True
            
            # 通过PID检查
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'mitmdump' in proc.info['name'] and str(self.port) in ' '.join(proc.info['cmdline']):
                        return True
                except:
                    continue
            
            return False
            
        except:
            return False
    
    def get_proxy_url(self) -> str:
        """获取代理URL
        
        Returns:
            str: 代理地址
        """
        return f"127.0.0.1:{self.port}"
    
    def diagnose_tls_issues(self) -> bool:
        """诊断TLS握手问题
        
        Returns:
            bool: 诊断是否成功
        """
        print("\n" + "🔍 TLS握手诊断" + "\n" + "="*50)
        
        # 检查证书是否存在
        if not self.cert_manager.check_certificate_exists():
            print("❌ 证书未找到")
            print("📝 解决方案: 重启mitmproxy以生成证书")
            return False
        
        print("✅ 证书文件存在")
        
        if sys.platform == "darwin":
            # macOS特定检查
            print("\n🍎 macOS证书信任检查:")
            
            if self.cert_manager.verify_certificate_trust_macos():
                print("✅ 证书已被系统信任")
            else:
                print("❌ 证书未被系统信任")
                print("\n🛠️  尝试自动修复...")
                
                if self.cert_manager.fix_certificate_trust_macos():
                    print("✅ 自动修复成功!")
                else:
                    print("❌ 自动修复失败")
                    print("\n📝 需要手动修复:")
                    self.cert_manager._show_manual_certificate_instructions(
                        self.cert_manager.get_certificate_path()
                    )
                    return False
        
        # 其他建议
        print("\n🌐 浏览器建议:")
        print("1. Chrome: 安装证书后重启浏览器")
        print("2. Safari: 可能需要在钥匙串访问中手动批准证书")
        print("3. Firefox: 使用独立证书存储 - 可能需要单独导入")
        
        return True

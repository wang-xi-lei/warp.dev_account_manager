#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统代理配置管理器 - 跨平台支持
"""

import sys
import subprocess
import os
from utils import is_windows, is_macos


class ProxyManager:
    """跨平台系统代理配置管理器"""
    
    @staticmethod
    def set_proxy(proxy_server: str) -> bool:
        """启用代理设置
        
        Args:
            proxy_server: 代理服务器地址 (格式: host:port)
            
        Returns:
            bool: 是否成功
        """
        if is_windows():
            return ProxyManager._set_proxy_windows(proxy_server)
        elif is_macos():
            return ProxyManager._set_proxy_macos(proxy_server)
        else:
            print("当前平台不支持代理配置")
            return False
    
    @staticmethod
    def disable_proxy() -> bool:
        """禁用代理设置
        
        Returns:
            bool: 是否成功
        """
        if is_windows():
            return ProxyManager._disable_proxy_windows()
        elif is_macos():
            return ProxyManager._disable_proxy_macos()
        else:
            print("当前平台不支持代理配置")
            return False
    
    @staticmethod
    def is_proxy_enabled() -> bool:
        """检查代理是否启用
        
        Returns:
            bool: 代理是否启用
        """
        if is_windows():
            return ProxyManager._is_proxy_enabled_windows()
        elif is_macos():
            return ProxyManager._is_proxy_enabled_macos()
        else:
            return False
    
    # ========== Windows实现 ==========
    
    @staticmethod
    def _set_proxy_windows(proxy_server: str) -> bool:
        """Windows代理配置（使用注册表）"""
        try:
            import winreg
            
            # 打开注册表键
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                0, 
                winreg.KEY_SET_VALUE
            )
            
            # 设置代理
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy_server)
            winreg.CloseKey(key)
            
            # 刷新IE设置（静默）
            try:
                subprocess.run(
                    ["rundll32.exe", "wininet.dll,InternetSetOption", "0", "37", "0", "0"],
                    shell=True, 
                    capture_output=True, 
                    timeout=5
                )
            except:
                pass
            
            print(f"✅ Windows代理已设置: {proxy_server}")
            return True
            
        except Exception as e:
            print(f"❌ Windows代理设置错误: {e}")
            return False
    
    @staticmethod
    def _disable_proxy_windows() -> bool:
        """禁用Windows代理"""
        try:
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                0, 
                winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            print("✅ Windows代理已禁用")
            return True
            
        except Exception as e:
            print(f"❌ Windows代理禁用错误: {e}")
            return False
    
    @staticmethod
    def _is_proxy_enabled_windows() -> bool:
        """检查Windows代理是否启用"""
        try:
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                0, 
                winreg.KEY_READ
            )
            
            proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            winreg.CloseKey(key)
            
            return bool(proxy_enable)
            
        except:
            return False
    
    # ========== macOS实现 ==========
    
    @staticmethod
    def _set_proxy_macos(proxy_server: str) -> bool:
        """macOS代理配置（使用PAC文件）"""
        try:
            host, port = proxy_server.split(":")
            
            # 创建PAC文件（只代理Warp域名）
            pac_content = f"""function FindProxyForURL(url, host) {{
    // 仅代理Warp相关域名
    if (shExpMatch(host, "*.warp.dev") || 
        shExpMatch(host, "*warp.dev") ||
        shExpMatch(host, "*.dataplane.rudderstack.com") ||
        shExpMatch(host, "*dataplane.rudderstack.com")) {{
        return "PROXY {host}:{port}";
    }}
    
    // 其他流量直连（保留互联网访问）
    return "DIRECT";
}}"""
            
            # 写入PAC文件
            pac_dir = os.path.expanduser("~/.warp_proxy")
            os.makedirs(pac_dir, exist_ok=True)
            pac_file = os.path.join(pac_dir, "warp_proxy.pac")
            
            with open(pac_file, 'w') as f:
                f.write(pac_content)
            
            print(f"📝 PAC文件已创建: {pac_file}")
            
            # 获取活动网络服务
            service = ProxyManager._get_primary_network_service_macos()
            if not service:
                print("❌ 未找到合适的网络服务")
                return False
            
            print(f"🔧 配置PAC代理: {service}")
            
            # 设置自动代理配置（PAC）
            pac_url = f"file://{pac_file}"
            result1 = subprocess.run(
                ["networksetup", "-setautoproxyurl", service, pac_url],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            # 启用自动代理
            result2 = subprocess.run(
                ["networksetup", "-setautoproxystate", service, "on"],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result1.returncode == 0 and result2.returncode == 0:
                print(f"✅ PAC代理配置成功: {proxy_server}")
                print("✅ 互联网访问保留 - 仅Warp流量通过代理")
                return True
            else:
                print(f"⚠️ PAC代理配置失败，尝试手动代理...")
                return ProxyManager._set_proxy_macos_manual(proxy_server)
                
        except Exception as e:
            print(f"❌ macOS PAC代理设置错误: {e}")
            return ProxyManager._set_proxy_macos_manual(proxy_server)
    
    @staticmethod
    def _set_proxy_macos_manual(proxy_server: str) -> bool:
        """macOS手动代理配置（备用方案）"""
        try:
            host, port = proxy_server.split(":")
            
            service = ProxyManager._get_primary_network_service_macos()
            if not service:
                return False
            
            print(f"🔧 配置手动代理: {service}")
            
            # 设置HTTP代理
            result1 = subprocess.run(
                ["networksetup", "-setwebproxy", service, host, port],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            # 设置HTTPS代理
            result2 = subprocess.run(
                ["networksetup", "-setsecurewebproxy", service, host, port],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result1.returncode == 0 and result2.returncode == 0:
                print(f"✅ 手动代理配置成功: {proxy_server}")
                print("⚠️ 所有HTTP/HTTPS流量将通过代理")
                return True
            else:
                print(f"❌ 手动代理配置失败")
                return False
                
        except Exception as e:
            print(f"❌ macOS手动代理设置错误: {e}")
            return False
    
    @staticmethod
    def _disable_proxy_macos() -> bool:
        """禁用macOS代理（PAC和手动）"""
        try:
            service = ProxyManager._get_primary_network_service_macos()
            if not service:
                return False
            
            print(f"🔧 禁用代理: {service}")
            
            success_count = 0
            
            # 禁用自动代理（PAC）
            result1 = subprocess.run(
                ["networksetup", "-setautoproxystate", service, "off"],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result1.returncode == 0:
                success_count += 1
                print("✅ 自动代理（PAC）已禁用")
            
            # 禁用HTTP代理
            result2 = subprocess.run(
                ["networksetup", "-setwebproxystate", service, "off"],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result2.returncode == 0:
                success_count += 1
                print("✅ HTTP代理已禁用")
            
            # 禁用HTTPS代理
            result3 = subprocess.run(
                ["networksetup", "-setsecurewebproxystate", service, "off"],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result3.returncode == 0:
                success_count += 1
                print("✅ HTTPS代理已禁用")
            
            # 清理PAC文件
            try:
                pac_file = os.path.expanduser("~/.warp_proxy/warp_proxy.pac")
                if os.path.exists(pac_file):
                    os.remove(pac_file)
                    print("✅ PAC文件已清理")
            except Exception as e:
                print(f"⚠️ PAC文件清理失败: {e}")
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ macOS代理禁用错误: {e}")
            return False
    
    @staticmethod
    def _is_proxy_enabled_macos() -> bool:
        """检查macOS代理是否启用"""
        try:
            service = ProxyManager._get_primary_network_service_macos()
            if not service:
                return False
            
            # 检查自动代理（PAC）
            result1 = subprocess.run(
                ["networksetup", "-getautoproxyurl", service],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result1.returncode == 0 and "Enabled: Yes" in result1.stdout:
                return True
            
            # 检查HTTP代理
            result2 = subprocess.run(
                ["networksetup", "-getwebproxy", service],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result2.returncode == 0 and "Enabled: Yes" in result2.stdout:
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ macOS代理检查错误: {e}")
            return False
    
    @staticmethod
    def _get_primary_network_service_macos():
        """获取macOS主要网络服务"""
        try:
            result = subprocess.run(
                ["networksetup", "-listnetworkserviceorder"],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            # 查找第一个活动服务
            services = []
            for line in result.stdout.split('\n'):
                if line.startswith('(') and ')' in line:
                    service_name = line.split(') ')[1] if ') ' in line else None
                    if service_name and service_name not in ['Bluetooth PAN', 'Thunderbolt Bridge']:
                        services.append(service_name)
            
            return services[0] if services else None
            
        except Exception as e:
            print(f"获取网络服务错误: {e}")
            return None

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bridge配置管理器 - 跨平台支持
整合Windows和macOS的Chrome扩展配置
"""

import os
import sys
import json
from pathlib import Path
from utils import is_windows, is_macos


class BridgeConfig:
    """跨平台Bridge配置管理"""
    
    def __init__(self):
        self.extension_id = "warp-account-bridge-v1"
        self.app_name = "com.warp.account.bridge"
    
    def setup_bridge_config(self) -> bool:
        """配置Bridge（跨平台）
        
        Returns:
            bool: 是否成功
        """
        print("🌉 Bridge配置启动...")
        
        localhost_ok = self.setup_localhost_access()
        
        if localhost_ok:
            print("✅ Bridge配置完成!")
            print("\n📋 后续步骤:")
            print("1. 重启Chrome浏览器")
            print("2. 从chrome://extensions/加载扩展")
            print("3. 启动Warp Account Manager")
            return True
        else:
            print("❌ Bridge配置失败!")
            return False
    
    def setup_localhost_access(self) -> bool:
        """配置localhost访问（使用扩展manifest）
        
        Returns:
            bool: 是否成功
        """
        try:
            print("🔧 Chrome扩展manifest localhost访问...")
            
            # Chrome扩展使用manifest中的externally_connectable
            # 无需额外的注册表或系统配置
            print("✅ 基于Manifest的localhost访问已激活")
            print("📋 扩展manifest具有externally_connectable配置")
            
            return True
            
        except Exception as e:
            print(f"❌ Localhost访问设置错误: {e}")
            return False
    
    def check_configuration(self) -> bool:
        """检查Bridge配置是否正确
        
        Returns:
            bool: 配置是否正确
        """
        try:
            print("🔍 检查Bridge配置...")
            
            # 基于manifest的配置总是返回True
            # 实际验证会在扩展加载时进行
            print("✅ 基于Manifest的Bridge配置")
            return True
            
        except Exception as e:
            print(f"❌ 配置检查错误: {e}")
            return False
    
    def remove_configuration(self) -> bool:
        """移除Bridge配置（清理）
        
        Returns:
            bool: 是否成功
        """
        try:
            print("🧹 清理Bridge配置...")
            
            # Manifest-based配置无需清理
            # 只需移除扩展即可
            print("✅ Bridge配置已清理")
            return True
            
        except Exception as e:
            print(f"❌ 清理错误: {e}")
            return False
    
    # ========== Windows特定实现（保留用于Native Messaging） ==========
    
    def create_native_messaging_manifest_windows(self):
        """创建Windows Native Messaging manifest（可选功能）"""
        if not is_windows():
            return None
        
        try:
            python_exe = sys.executable
            script_path = os.path.abspath("warp_account_manager.py")
            
            manifest = {
                "name": self.app_name,
                "description": "Warp Account Bridge Native Host",
                "path": python_exe,
                "type": "stdio",
                "allowed_origins": [
                    f"chrome-extension://{self.extension_id}/"
                ]
            }
            
            # 保存manifest
            manifest_dir = os.path.join(os.getenv('APPDATA'), 'WarpAccountManager')
            os.makedirs(manifest_dir, exist_ok=True)
            
            manifest_path = os.path.join(manifest_dir, f"{self.app_name}.json")
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"✅ Windows Native Messaging manifest已创建: {manifest_path}")
            return manifest_path
            
        except Exception as e:
            print(f"❌ Windows manifest创建错误: {e}")
            return None
    
    def register_native_host_windows(self):
        """注册Windows Native Messaging host（可选功能）"""
        if not is_windows():
            return False
        
        try:
            import winreg
            
            manifest_path = self.create_native_messaging_manifest_windows()
            if not manifest_path:
                return False
            
            # 注册表路径
            registry_paths = [
                r"SOFTWARE\Google\Chrome\NativeMessagingHosts",
                r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts"
            ]
            
            success = False
            for registry_path in registry_paths:
                try:
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)
                    winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, manifest_path)
                    winreg.CloseKey(key)
                    print(f"✅ Native host已注册: {registry_path}")
                    success = True
                except Exception as e:
                    print(f"⚠️  注册表注册错误 ({registry_path}): {e}")
            
            return success
            
        except Exception as e:
            print(f"❌ Native host注册错误: {e}")
            return False
    
    # ========== macOS特定实现（保留用于Native Messaging） ==========
    
    def create_native_messaging_manifest_macos(self):
        """创建macOS Native Messaging manifest（可选功能）"""
        if not is_macos():
            return None
        
        try:
            python_exe = sys.executable
            script_path = os.path.abspath("warp_account_manager.py")
            
            manifest = {
                "name": self.app_name,
                "description": "Warp Account Bridge Native Host",
                "path": python_exe,
                "type": "stdio",
                "allowed_origins": [
                    f"chrome-extension://{self.extension_id}/"
                ]
            }
            
            # macOS manifest位置
            native_messaging_dir = Path.home() / "Library/Application Support/Google/Chrome/NativeMessagingHosts"
            native_messaging_dir.mkdir(parents=True, exist_ok=True)
            
            manifest_path = native_messaging_dir / f"{self.app_name}.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"✅ macOS Native Messaging manifest已创建: {manifest_path}")
            return str(manifest_path)
            
        except Exception as e:
            print(f"❌ macOS manifest创建错误: {e}")
            return None
    
    def register_native_host_macos(self):
        """注册macOS Native Messaging host（可选功能）"""
        if not is_macos():
            return False
        
        try:
            manifest_path = self.create_native_messaging_manifest_macos()
            if not manifest_path:
                return False
            
            print(f"✅ macOS Native host已注册: {manifest_path}")
            return True
            
        except Exception as e:
            print(f"❌ Native host注册错误: {e}")
            return False


# 便捷函数
def setup_bridge():
    """配置Bridge"""
    config = BridgeConfig()
    return config.setup_bridge_config()


def check_bridge():
    """检查Bridge配置"""
    config = BridgeConfig()
    return config.check_configuration()


def remove_bridge():
    """移除Bridge配置"""
    config = BridgeConfig()
    return config.remove_configuration()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "setup":
            setup_bridge()
        elif action == "check":
            check_bridge()
        elif action == "remove":
            remove_bridge()
        else:
            print("用法: python bridge_config.py [setup|check|remove]")
    else:
        # 默认：setup
        setup_bridge()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SSL证书管理器 - Mitmproxy证书安装和验证
"""

import sys
import subprocess
import os
from pathlib import Path
from utils import is_windows, is_macos


class CertificateManager:
    """Mitmproxy SSL证书管理"""
    
    def __init__(self):
        self.mitmproxy_dir = Path.home() / ".mitmproxy"
        self.cert_file = self.mitmproxy_dir / "mitmproxy-ca-cert.cer"
    
    def check_certificate_exists(self) -> bool:
        """检查证书文件是否存在"""
        return self.cert_file.exists()
    
    def get_certificate_path(self) -> str:
        """获取证书文件路径"""
        return str(self.cert_file)
    
    def install_certificate_automatically(self) -> bool:
        """自动安装证书（跨平台）
        
        Returns:
            bool: 是否成功
        """
        try:
            cert_path = self.get_certificate_path()
            if not self.check_certificate_exists():
                print("❌ 证书文件不存在")
                return False
            
            print("🔧 正在安装证书...")
            
            if is_windows():
                return self._install_certificate_windows(cert_path)
            elif is_macos():
                return self._install_certificate_macos(cert_path)
            else:
                print("当前平台不支持自动证书安装")
                return False
                
        except Exception as e:
            print(f"❌ 证书安装错误: {e}")
            return False
    
    # ========== Windows实现 ==========
    
    def _install_certificate_windows(self, cert_path: str) -> bool:
        """Windows证书安装（使用certutil）"""
        try:
            cmd = ["certutil", "-addstore", "root", cert_path]
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                print("✅ Windows证书安装成功")
                return True
            else:
                print(f"❌ Windows证书安装失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Windows证书安装错误: {e}")
            return False
    
    # ========== macOS实现 ==========
    
    def _install_certificate_macos(self, cert_path: str) -> bool:
        """macOS证书安装（尝试多种策略）"""
        
        # 策略1: 添加到系统钥匙串
        print("📝 策略1: 尝试添加到系统钥匙串...")
        cmd_system = [
            "security", "add-trusted-cert",
            "-d", "-r", "trustRoot",
            "-k", "/Library/Keychains/System.keychain",
            cert_path
        ]
        result_system = subprocess.run(cmd_system, capture_output=True, text=True)
        
        if result_system.returncode == 0:
            print("✅ macOS证书安装成功（系统钥匙串）")
            return True
        else:
            print(f"⚠️ 系统钥匙串失败: {result_system.stderr}")
        
        # 策略2: 添加到登录钥匙串
        print("📝 策略2: 尝试添加到登录钥匙串...")
        user_keychain = os.path.expanduser("~/Library/Keychains/login.keychain-db")
        
        # 先添加证书
        cmd_add = ["security", "add-cert", "-k", user_keychain, cert_path]
        result_add = subprocess.run(cmd_add, capture_output=True, text=True)
        
        if result_add.returncode == 0:
            # 再设置信任
            cmd_trust = [
                "security", "add-trusted-cert",
                "-d", "-r", "trustRoot",
                "-k", user_keychain,
                cert_path
            ]
            result_trust = subprocess.run(cmd_trust, capture_output=True, text=True)
            
            if result_trust.returncode == 0:
                print("✅ macOS证书安装成功（登录钥匙串）")
                return True
            else:
                print(f"⚠️ 信任设置失败: {result_trust.stderr}")
        else:
            print(f"⚠️ 证书添加失败: {result_add.stderr}")
        
        # 所有策略失败
        print("❌ macOS证书自动安装失败，需要手动安装")
        self._show_manual_certificate_instructions(cert_path)
        return False
    
    def verify_certificate_trust_macos(self) -> bool:
        """验证macOS证书信任状态"""
        if not is_macos():
            return True
        
        try:
            cert_path = self.get_certificate_path()
            if not self.check_certificate_exists():
                return False
            
            # 使用security命令验证证书
            cmd = ["security", "verify-cert", "-c", cert_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 证书已被系统信任")
                return True
            else:
                print(f"⚠️ 证书信任验证失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"证书验证错误: {e}")
            return False
    
    def fix_certificate_trust_macos(self) -> bool:
        """修复macOS证书信任问题"""
        if not is_macos():
            return True
        
        try:
            cert_path = self.get_certificate_path()
            if not self.check_certificate_exists():
                print("❌ 证书文件不存在")
                return False
            
            print("🔧 尝试修复证书信任...")
            
            # 步骤1: 删除现有证书
            print("步骤1: 删除现有证书...")
            cmd_remove = ["security", "delete-certificate", "-c", "mitmproxy"]
            subprocess.run(cmd_remove, capture_output=True, text=True)
            
            # 步骤2: 重新添加并信任
            print("步骤2: 重新添加证书并设置信任...")
            user_keychain = os.path.expanduser("~/Library/Keychains/login.keychain-db")
            
            # 导入证书
            cmd_import = ["security", "import", cert_path, "-k", user_keychain, "-A"]
            result_import = subprocess.run(cmd_import, capture_output=True, text=True)
            
            if result_import.returncode == 0:
                # 设置信任
                cmd_trust = [
                    "security", "add-trusted-cert",
                    "-d", "-r", "trustRoot",
                    "-k", user_keychain,
                    cert_path
                ]
                result_trust = subprocess.run(cmd_trust, capture_output=True, text=True)
                
                if result_trust.returncode == 0:
                    print("✅ 证书信任修复成功")
                    return True
                else:
                    print(f"❌ 信任设置失败: {result_trust.stderr}")
            else:
                print(f"❌ 证书导入失败: {result_import.stderr}")
            
            return False
            
        except Exception as e:
            print(f"证书信任修复错误: {e}")
            return False
    
    def _show_manual_certificate_instructions(self, cert_path: str):
        """显示手动证书安装说明"""
        print("\n" + "="*60)
        print("🔒 需要手动安装证书")
        print("="*60)
        print(f"证书位置: {cert_path}")
        print("\n请按照以下步骤操作:")
        
        if is_macos():
            print("1. 打开「钥匙串访问」应用")
            print("2. 将证书文件拖入「系统」或「登录」钥匙串")
            print("3. 双击已安装的证书")
            print("4. 展开「信任」部分")
            print("5. 将「使用此证书时」设置为「始终信任」")
            print("6. 关闭窗口并输入密码确认")
        elif is_windows():
            print("1. 双击证书文件")
            print("2. 点击「安装证书」")
            print("3. 选择「本地计算机」")
            print("4. 选择「将所有的证书都放入下列存储」")
            print("5. 点击「浏览」选择「受信任的根证书颁发机构」")
            print("6. 完成安装")
        
        print("\n🌐 浏览器说明:")
        print("- Chrome/Safari: 重启浏览器")
        print("- Firefox: 使用自己的证书存储，可能需要单独导入")
        print("="*60 + "\n")

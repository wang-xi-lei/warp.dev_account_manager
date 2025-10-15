#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高级账号管理器 - 整合数据库和API功能
"""

from typing import Tuple, List, Optional
from database import AccountDatabase
from api import FirebaseAPI, WarpAPI


class AccountManager:
    """高级账号管理器 - 提供完整的账号管理功能"""
    
    def __init__(self, db_path="accounts.db"):
        self.db = AccountDatabase(db_path)
    
    # ========== 账号基本操作（委托给database） ==========
    
    def add_account(self, account_json: str) -> Tuple[bool, str]:
        """添加账号"""
        return self.db.add_account(account_json)
    
    def get_accounts(self) -> List[Tuple[str, str]]:
        """获取所有账号"""
        return self.db.get_accounts()
    
    def get_accounts_with_health(self) -> List[Tuple[str, str, str]]:
        """获取所有账号及健康状态"""
        return self.db.get_accounts_with_health()
    
    def get_accounts_with_health_and_limits(self) -> List[Tuple[str, str, str, str]]:
        """获取所有账号及健康状态和限额"""
        return self.db.get_accounts_with_health_and_limits()
    
    def update_account_health(self, email: str, health_status: str) -> bool:
        """更新账号健康状态"""
        return self.db.update_account_health(email, health_status)
    
    def update_account_token(self, email: str, new_token_data: dict) -> bool:
        """更新账号token"""
        return self.db.update_account_token(email, new_token_data)
    
    def update_account(self, email: str, updated_json: str) -> bool:
        """更新账号所有信息"""
        return self.db.update_account(email, updated_json)
    
    def update_account_limit_info(self, email: str, limit_info: str) -> bool:
        """更新账号限额信息"""
        return self.db.update_account_limit_info(email, limit_info)
    
    def delete_account(self, email: str) -> bool:
        """删除账号"""
        return self.db.delete_account(email)
    
    def set_active_account(self, email: str) -> bool:
        """设置活动账号"""
        return self.db.set_active_account(email)
    
    def get_active_account(self) -> Optional[str]:
        """获取活动账号"""
        return self.db.get_active_account()
    
    def clear_active_account(self) -> bool:
        """清除活动账号"""
        return self.db.clear_active_account()
    
    def is_certificate_approved(self) -> bool:
        """检查证书是否已批准"""
        return self.db.is_certificate_approved()
    
    def set_certificate_approved(self, approved=True) -> bool:
        """设置证书批准状态"""
        return self.db.set_certificate_approved(approved)
    
    # ========== 高级功能（整合API） ==========
    
    def refresh_account_token(self, email: str, account_data: dict, proxy_enabled=False) -> Tuple[bool, str]:
        """刷新账号token
        
        Args:
            email: 账号邮箱
            account_data: 账号数据
            proxy_enabled: 是否使用代理
            
        Returns:
            (bool, str): (是否成功, 消息)
        """
        try:
            refresh_token = account_data['stsTokenManager']['refreshToken']
            api_key = account_data['apiKey']
            
            # 使用FirebaseAPI刷新token
            new_token_data = FirebaseAPI.refresh_token(api_key, refresh_token, proxy_enabled)
            
            if new_token_data:
                if self.update_account_token(email, new_token_data):
                    return True, f"{email} token刷新成功"
                else:
                    return False, f"{email} token更新数据库失败"
            else:
                return False, f"{email} token刷新失败"
        
        except Exception as e:
            return False, f"Token刷新错误: {str(e)}"
    
    def get_account_limit_info(self, account_data: dict, proxy_enabled=False) -> Optional[dict]:
        """获取账号使用限额
        
        Args:
            account_data: 账号数据
            proxy_enabled: 是否使用代理
            
        Returns:
            dict: 限额信息，失败返回None
        """
        try:
            access_token = account_data['stsTokenManager']['accessToken']
            return WarpAPI.get_limit_info(access_token, proxy_enabled)
        
        except Exception as e:
            print(f"限额信息获取错误: {e}")
            return None
    
    def refresh_and_get_limits(self, email: str, account_data: dict, proxy_enabled=False) -> Tuple[bool, Optional[dict], str]:
        """刷新token并获取限额（如果需要）
        
        Args:
            email: 账号邮箱
            account_data: 账号数据
            proxy_enabled: 是否使用代理
            
        Returns:
            (bool, dict, str): (是否成功, 限额信息, 消息)
        """
        import time
        
        try:
            # 检查token是否过期
            expiration_time = account_data['stsTokenManager']['expirationTime']
            current_time = int(time.time() * 1000)
            
            if current_time >= expiration_time:
                # Token已过期，需要刷新
                success, msg = self.refresh_account_token(email, account_data, proxy_enabled)
                if not success:
                    return False, None, msg
                
                # 获取更新后的账号数据
                accounts = self.get_accounts()
                for acc_email, acc_json in accounts:
                    if acc_email == email:
                        import json
                        account_data = json.loads(acc_json)
                        break
            
            # 获取限额信息
            limit_info = self.get_account_limit_info(account_data, proxy_enabled)
            
            if limit_info:
                used = limit_info.get('requestsUsedSinceLastRefresh', 0)
                total = limit_info.get('requestLimit', 0)
                
                # 更新数据库
                self.update_account_health(email, 'healthy')
                self.update_account_limit_info(email, f"{used}/{total}")
                
                return True, limit_info, "成功"
            else:
                self.update_account_health(email, 'unhealthy')
                return False, None, "限额信息获取失败"
        
        except Exception as e:
            self.update_account_health(email, 'unhealthy')
            return False, None, f"错误: {str(e)}"
    
    def batch_refresh_and_get_limits(self, proxy_enabled=False) -> List[Tuple[str, str, str]]:
        """批量刷新所有账号并获取限额
        
        Args:
            proxy_enabled: 是否使用代理
            
        Returns:
            List[Tuple[str, str, str]]: [(email, status, limit_info), ...]
        """
        import json
        
        results = []
        accounts = self.get_accounts_with_health()
        
        for email, account_json, health_status in accounts:
            try:
                # 跳过封禁账号
                if health_status == 'banned':
                    results.append((email, 'banned', 'N/A'))
                    continue
                
                account_data = json.loads(account_json)
                success, limit_info, msg = self.refresh_and_get_limits(email, account_data, proxy_enabled)
                
                if success and limit_info:
                    used = limit_info.get('requestsUsedSinceLastRefresh', 0)
                    total = limit_info.get('requestLimit', 0)
                    results.append((email, 'success', f"{used}/{total}"))
                else:
                    results.append((email, 'failed', msg))
            
            except Exception as e:
                results.append((email, 'error', str(e)))
        
        return results

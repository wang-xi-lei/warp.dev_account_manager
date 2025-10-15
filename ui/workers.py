#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
后台工作线程 - QThread Workers
"""

import json
import time
from PyQt5.QtCore import QThread, pyqtSignal
from database import AccountDatabase
from api import FirebaseAPI, WarpAPI
from utils import get_os_info
from languages import _


class TokenWorker(QThread):
    """单个token刷新的后台工作线程"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)  # success, message
    error = pyqtSignal(str)
    
    def __init__(self, email, account_data, proxy_enabled=False):
        super().__init__()
        self.email = email
        self.account_data = account_data
        self.db = AccountDatabase()
        self.proxy_enabled = proxy_enabled
    
    def run(self):
        """执行token刷新"""
        try:
            self.progress.emit(f"Token刷新中: {self.email}")
            
            if self.refresh_token():
                self.db.update_account_health(self.email, 'healthy')
                self.finished.emit(True, f"{self.email} token刷新成功")
            else:
                self.db.update_account_health(self.email, 'unhealthy')
                self.finished.emit(False, f"{self.email} token刷新失败")
        
        except Exception as e:
            self.error.emit(f"Token刷新错误: {str(e)}")
    
    def refresh_token(self) -> bool:
        """刷新Firebase token"""
        try:
            refresh_token = self.account_data['stsTokenManager']['refreshToken']
            api_key = self.account_data['apiKey']
            
            # 使用FirebaseAPI刷新token
            new_token_data = FirebaseAPI.refresh_token(api_key, refresh_token, self.proxy_enabled)
            
            if new_token_data:
                return self.db.update_account_token(self.email, new_token_data)
            return False
        
        except Exception as e:
            print(f"Token刷新错误: {e}")
            return False


class TokenRefreshWorker(QThread):
    """批量token刷新和限额获取的后台工作线程"""
    
    progress = pyqtSignal(int, str)  # percentage, message
    finished = pyqtSignal(list)  # results
    error = pyqtSignal(str)
    
    def __init__(self, accounts, proxy_enabled=False):
        super().__init__()
        self.accounts = accounts
        self.db = AccountDatabase()
        self.proxy_enabled = proxy_enabled
    
    def run(self):
        """执行批量token刷新和限额获取"""
        results = []
        total_accounts = len(self.accounts)
        
        for i, (email, account_json, health_status) in enumerate(self.accounts):
            try:
                self.progress.emit(
                    int((i / total_accounts) * 100),
                    _('processing_account', email)
                )
                
                # 跳过已封禁账号
                if health_status == _('status_banned_key'):
                    self.db.update_account_limit_info(email, _('status_na'))
                    results.append((email, _('status_banned'), _('status_na')))
                    continue
                
                account_data = json.loads(account_json)
                
                # 检查token是否过期
                expiration_time = account_data['stsTokenManager']['expirationTime']
                current_time = int(time.time() * 1000)
                
                if current_time >= expiration_time:
                    # Token已过期，刷新
                    self.progress.emit(
                        int((i / total_accounts) * 100),
                        _('refreshing_token', email)
                    )
                    
                    if not self.refresh_token(email, account_data):
                        # Token刷新失败
                        self.db.update_account_health(email, _('status_unhealthy'))
                        self.db.update_account_limit_info(email, _('status_na'))
                        results.append((email, _('token_refresh_failed', email), _('status_na')))
                        continue
                    
                    # 获取更新后的account_data
                    updated_accounts = self.db.get_accounts()
                    for updated_email, updated_json in updated_accounts:
                        if updated_email == email:
                            account_data = json.loads(updated_json)
                            break
                
                # 获取限额信息
                limit_info = self.get_limit_info(account_data)
                if limit_info:
                    used = limit_info.get('requestsUsedSinceLastRefresh', 0)
                    total = limit_info.get('requestLimit', 0)
                    limit_text = f"{used}/{total}"
                    
                    # 更新为健康状态
                    self.db.update_account_health(email, _('status_healthy'))
                    self.db.update_account_limit_info(email, limit_text)
                    results.append((email, _('success'), limit_text))
                else:
                    # 限额获取失败
                    self.db.update_account_health(email, _('status_unhealthy'))
                    self.db.update_account_limit_info(email, _('status_na'))
                    results.append((email, _('limit_info_failed'), _('status_na')))
            
            except Exception as e:
                self.db.update_account_limit_info(email, _('status_na'))
                results.append((email, f"{_('error')}: {str(e)}", _('status_na')))
        
        self.finished.emit(results)
    
    def refresh_token(self, email, account_data) -> bool:
        """刷新Firebase token"""
        try:
            refresh_token = account_data['stsTokenManager']['refreshToken']
            api_key = account_data['apiKey']
            
            # 使用FirebaseAPI刷新token
            new_token_data = FirebaseAPI.refresh_token(api_key, refresh_token, self.proxy_enabled)
            
            if new_token_data:
                return self.db.update_account_token(email, new_token_data)
            return False
        
        except Exception as e:
            print(f"Token刷新错误: {e}")
            return False
    
    def get_limit_info(self, account_data):
        """从Warp API获取限额信息"""
        try:
            access_token = account_data['stsTokenManager']['accessToken']
            
            # 使用WarpAPI获取限额
            return WarpAPI.get_limit_info(access_token, self.proxy_enabled)
        
        except Exception as e:
            print(f"限额信息获取错误: {e}")
            return None

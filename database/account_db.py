#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
账号数据库管理
"""

import sqlite3
import json
from typing import List, Tuple, Optional
from languages import _


class AccountDatabase:
    """账号数据库管理类"""
    
    def __init__(self, db_path="accounts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库并创建表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建账号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                account_data TEXT NOT NULL,
                health_status TEXT DEFAULT 'healthy',
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 添加health_status列（如果不存在）
        try:
            cursor.execute('ALTER TABLE accounts ADD COLUMN health_status TEXT DEFAULT "healthy"')
        except sqlite3.OperationalError:
            pass
        
        # 添加limit_info列（如果不存在）
        try:
            cursor.execute('ALTER TABLE accounts ADD COLUMN limit_info TEXT DEFAULT "Güncellenmedi"')
        except sqlite3.OperationalError:
            pass
        
        # 创建代理设置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxy_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # 设置默认值
        cursor.execute('''
            INSERT OR IGNORE INTO proxy_settings (key, value)
            VALUES ('certificate_approved', 'false')
        ''')
        
        conn.commit()
        conn.close()
    
    def add_account(self, account_json: str) -> Tuple[bool, str]:
        """添加账号"""
        try:
            account_data = json.loads(account_json)
            email = account_data.get('email')
            
            if not email:
                raise ValueError(_('email_not_found'))
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO accounts (email, account_data, last_updated)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (email, account_json))
            conn.commit()
            conn.close()
            return True, _('account_added_success')
        except json.JSONDecodeError:
            return False, _('invalid_json')
        except Exception as e:
            return False, f"{_('error')}: {str(e)}"
    
    def get_accounts(self) -> List[Tuple[str, str]]:
        """获取所有账号"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT email, account_data FROM accounts ORDER BY email')
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    
    def get_accounts_with_health(self) -> List[Tuple[str, str, str]]:
        """获取所有账号及健康状态"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT email, account_data, health_status FROM accounts ORDER BY email')
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    
    def get_accounts_with_health_and_limits(self) -> List[Tuple[str, str, str, str]]:
        """获取所有账号及健康状态和限制信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT email, account_data, health_status, limit_info FROM accounts ORDER BY email')
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    
    def update_account_health(self, email: str, health_status: str) -> bool:
        """更新账号健康状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE accounts SET health_status = ?, last_updated = CURRENT_TIMESTAMP
                WHERE email = ?
            ''', (health_status, email))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"健康状态更新错误: {e}")
            return False
    
    def update_account_token(self, email: str, new_token_data: dict) -> bool:
        """更新账号token信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT account_data FROM accounts WHERE email = ?', (email,))
            result = cursor.fetchone()
            
            if result:
                account_data = json.loads(result[0])
                account_data['stsTokenManager'].update(new_token_data)
                
                cursor.execute('''
                    UPDATE accounts SET account_data = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE email = ?
                ''', (json.dumps(account_data), email))
                conn.commit()
                conn.close()
                return True
            return False
        except Exception as e:
            print(f"Token更新错误: {e}")
            return False
    
    def update_account(self, email: str, updated_json: str) -> bool:
        """更新账号所有信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE accounts SET account_data = ?, last_updated = CURRENT_TIMESTAMP
                WHERE email = ?
            ''', (updated_json, email))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"账号更新错误: {e}")
            return False
    
    def update_account_limit_info(self, email: str, limit_info: str) -> bool:
        """更新账号限制信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE accounts SET limit_info = ?, last_updated = CURRENT_TIMESTAMP
                WHERE email = ?
            ''', (limit_info, email))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"限制信息更新错误: {e}")
            return False
    
    def delete_account(self, email: str) -> bool:
        """删除账号"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 删除账号
            cursor.execute('DELETE FROM accounts WHERE email = ?', (email,))
            
            # 如果删除的是活动账号，清除活动账号设置
            cursor.execute('SELECT value FROM proxy_settings WHERE key = ?', ('active_account',))
            result = cursor.fetchone()
            if result and result[0] == email:
                cursor.execute('DELETE FROM proxy_settings WHERE key = ?', ('active_account',))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"账号删除错误: {e}")
            return False
    
    def set_active_account(self, email: str) -> bool:
        """设置活动账号"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO proxy_settings (key, value)
                VALUES ('active_account', ?)
            ''', (email,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"活动账号设置错误: {e}")
            return False
    
    def get_active_account(self) -> Optional[str]:
        """获取活动账号"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM proxy_settings WHERE key = ?', ('active_account',))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except:
            return None
    
    def clear_active_account(self) -> bool:
        """清除活动账号"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM proxy_settings WHERE key = ?', ('active_account',))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"活动账号清除错误: {e}")
            return False
    
    def is_certificate_approved(self) -> bool:
        """检查证书是否已批准"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM proxy_settings WHERE key = ?', ('certificate_approved',))
            result = cursor.fetchone()
            conn.close()
            return result and result[0] == 'true'
        except:
            return False
    
    def set_certificate_approved(self, approved=True) -> bool:
        """设置证书批准状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO proxy_settings (key, value)
                VALUES ('certificate_approved', ?)
            ''', ('true' if approved else 'false',))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"证书批准状态保存错误: {e}")
            return False

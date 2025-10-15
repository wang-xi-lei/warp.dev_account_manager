#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Firebase认证API客户端
"""

import time
import requests


class FirebaseAPI:
    """Firebase认证API管理"""
    
    @staticmethod
    def refresh_token(api_key: str, refresh_token: str, proxy_enabled=False) -> dict:
        """刷新Firebase token
        
        Args:
            api_key: Firebase API密钥
            refresh_token: 刷新token
            proxy_enabled: 是否使用代理
            
        Returns:
            dict: 新的token数据或None
        """
        try:
            url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'WarpAccountManager/1.0'
            }
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
            
            # 代理设置
            proxies = {'http': None, 'https': None} if proxy_enabled else None
            response = requests.post(
                url, 
                json=data, 
                headers=headers, 
                timeout=30,
                verify=not proxy_enabled, 
                proxies=proxies
            )
            
            if response.status_code == 200:
                token_data = response.json()
                return {
                    'accessToken': token_data['access_token'],
                    'refreshToken': token_data['refresh_token'],
                    'expirationTime': int(time.time() * 1000) + (int(token_data['expires_in']) * 1000)
                }
            return None
        except Exception as e:
            print(f"Token刷新错误: {e}")
            return None

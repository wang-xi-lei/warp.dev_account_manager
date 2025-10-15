#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Warp API客户端
"""

import requests
from utils.os_utils import get_os_info


class WarpAPI:
    """Warp API管理"""
    
    BASE_URL = "https://app.warp.dev/graphql/v2"
    
    @staticmethod
    def get_limit_info(access_token: str, proxy_enabled=False) -> dict:
        """获取账号使用限制信息
        
        Args:
            access_token: 访问token
            proxy_enabled: 是否使用代理
            
        Returns:
            dict: 限制信息或None
        """
        try:
            os_info = get_os_info()
            
            url = f"{WarpAPI.BASE_URL}?op=GetRequestLimitInfo"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
                'X-Warp-Client-Version': 'v0.2025.08.27.08.11.stable_04',
                'X-Warp-Os-Category': os_info['category'],
                'X-Warp-Os-Name': os_info['name'],
                'X-Warp-Os-Version': os_info['version'],
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Warp-Manager-Request': 'true'
            }
            
            query = """
            query GetRequestLimitInfo($requestContext: RequestContext!) {
              user(requestContext: $requestContext) {
                __typename
                ... on UserOutput {
                  user {
                    requestLimitInfo {
                      isUnlimited
                      nextRefreshTime
                      requestLimit
                      requestsUsedSinceLastRefresh
                      requestLimitRefreshDuration
                      isUnlimitedAutosuggestions
                      acceptedAutosuggestionsLimit
                      acceptedAutosuggestionsSinceLastRefresh
                      isUnlimitedVoice
                      voiceRequestLimit
                      voiceRequestsUsedSinceLastRefresh
                      voiceTokenLimit
                      voiceTokensUsedSinceLastRefresh
                      isUnlimitedCodebaseIndices
                      maxCodebaseIndices
                      maxFilesPerRepo
                      embeddingGenerationBatchSize
                    }
                  }
                }
                ... on UserFacingError {
                  error {
                    __typename
                    ... on SharedObjectsLimitExceeded {
                      limit
                      objectType
                      message
                    }
                    ... on PersonalObjectsLimitExceeded {
                      limit
                      objectType
                      message
                    }
                    ... on AccountDelinquencyError {
                      message
                    }
                    ... on GenericStringObjectUniqueKeyConflict {
                      message
                    }
                  }
                  responseContext {
                    serverVersion
                  }
                }
              }
            }
            """
            
            payload = {
                "query": query,
                "variables": {
                    "requestContext": {
                        "clientContext": {
                            "version": "v0.2025.08.27.08.11.stable_04"
                        },
                        "osContext": {
                            "category": os_info['category'],
                            "linuxKernelVersion": None,
                            "name": os_info['category'],
                            "version": os_info['version']
                        }
                    }
                },
                "operationName": "GetRequestLimitInfo"
            }
            
            # 代理设置
            proxies = {'http': None, 'https': None} if proxy_enabled else None
            response = requests.post(
                url, 
                headers=headers, 
                json=payload, 
                timeout=30,
                verify=not proxy_enabled, 
                proxies=proxies
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user_data = data['data']['user']
                    if user_data.get('__typename') == 'UserOutput':
                        return user_data['user']['requestLimitInfo']
            return None
        except Exception as e:
            print(f"限制信息获取错误: {e}")
            return None

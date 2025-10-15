#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
操作系统相关工具函数
"""

import sys
import platform


def get_os_info():
    """获取操作系统信息用于API headers"""
    if sys.platform == "win32":
        return {
            'category': 'Windows',
            'name': 'Windows', 
            'version': f'{platform.release()} ({platform.version()})'
        }
    elif sys.platform == "darwin":
        return {
            'category': 'Darwin',
            'name': 'macOS',
            'version': platform.mac_ver()[0]
        }
    else:
        # Linux or other
        return {
            'category': 'Linux',
            'name': platform.system(),
            'version': platform.release()
        }


def is_windows():
    """检查是否为Windows系统"""
    return sys.platform == "win32"


def is_macos():
    """检查是否为macOS系统"""
    return sys.platform == "darwin"


def is_linux():
    """检查是否为Linux系统"""
    return sys.platform not in ["win32", "darwin"]

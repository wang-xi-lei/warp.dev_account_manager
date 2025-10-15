#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
网络相关工具函数
"""

import socket


def is_port_open(host, port, timeout=1):
    """检查端口是否打开"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

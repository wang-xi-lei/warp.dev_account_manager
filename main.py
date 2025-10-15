#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Warp Account Manager - 模块化入口文件

这是新的模块化入口点，使用重构后的模块结构。
旧版入口 warp_account_manager.py 仍可使用以保持兼容性。
"""

import sys
import os

# 确保可以导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from utils import load_stylesheet


def main():
    """主函数 - 启动应用"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║      Warp Account Manager - 模块化版本 v2.0               ║
║                                                            ║
║      使用模块化架构运行                                    ║
║      文档: MODULAR_GUIDE.md                                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("🚀 正在启动 Warp Account Manager...")
    print("📦 加载模块化组件...\n")
    
    # 初始化语言管理器
    from languages import get_language_manager
    lang_manager = get_language_manager()
    lang_manager.detect_system_language()
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("Warp Account Manager")
    
    # 加载样式
    load_stylesheet(app)
    
    print("✅ 核心模块已加载")
    print("   - database: 数据库层")
    print("   - api: API客户端")
    print("   - core: 业务逻辑")
    print("   - bridge: Bridge服务器")
    print("   - utils: 工具函数")
    
    # 导入并启动主窗口（使用新的模块化UI）
    print("\n🎨 加载用户界面...")
    try:
        # 使用新的模块化MainWindow
        from ui import MainWindow
        
        window = MainWindow()
        window.show()
        
        print("✅ 应用已启动!\n")
        
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ UI加载失败: {e}")
        print("💡 提示: 如果UI模块未找到，请使用旧版")
        print("   备用方式: python warp_account_manager.py")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 应用已关闭")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

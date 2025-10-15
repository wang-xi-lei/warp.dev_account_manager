"""
UI Utility Functions

This module contains utility functions for UI operations:
- load_stylesheet: Load and apply QSS stylesheet to application
"""

import os
from typing import Any
from languages import _


def load_stylesheet(app: Any) -> None:
    """Load and apply modern, compact QSS stylesheet to application
    
    Attempts to load stylesheet from style.qss file in the application directory.
    If the file exists, applies it to the application. Errors are printed but
    don't stop application execution.
    
    Args:
        app: QApplication instance to apply stylesheet to
        
    Example:
        >>> from PyQt5.QtWidgets import QApplication
        >>> app = QApplication([])
        >>> load_stylesheet(app)
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from utils/ to project root
        project_root = os.path.dirname(base_dir)
        style_path = os.path.join(project_root, "style.qss")
        
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        else:
            print(f"Style file not found at: {style_path}")
    except Exception as e:
        print(f"{_('stylesheet_load_error', e)}")

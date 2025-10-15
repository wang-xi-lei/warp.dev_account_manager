"""
UI Dialog Components for Warp Account Manager

This module contains all dialog windows used in the application:
- ManualCertificateDialog: Manual certificate installation guide
- AddAccountDialog: Add account via JSON or Chrome extension
- HelpDialog: Help and usage documentation

All dialogs use PyQt5 and support internationalization via languages.py
"""

import sys
import os
import subprocess
import webbrowser
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QWidget, QScrollArea,
                             QTabWidget, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from languages import _


class ManualCertificateDialog(QDialog):
    """Manual certificate installation dialog
    
    Shows step-by-step instructions for manually installing the mitmproxy
    SSL certificate on different platforms.
    """

    def __init__(self, cert_path: str, parent=None):
        """Initialize manual certificate dialog
        
        Args:
            cert_path: Path to the certificate file
            parent: Parent widget
        """
        super().__init__(parent)
        self.cert_path = cert_path
        self.setWindowTitle(_('cert_manual_title'))
        self.setGeometry(300, 300, 650, 550)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel(_('cert_manual_title'))
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #d32f2f; margin-bottom: 10px;")
        layout.addWidget(title)

        # Explanation
        explanation = QLabel(_('cert_manual_explanation'))
        explanation.setWordWrap(True)
        explanation.setStyleSheet("background: #fff3cd; padding: 15px; border-radius: 8px; border: 1px solid #ffeaa7;")
        layout.addWidget(explanation)

        # Certificate path
        path_label = QLabel(_('cert_manual_path'))
        path_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(path_label)

        path_display = QLabel(self.cert_path)
        path_display.setStyleSheet("""
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-family: 'Courier New', monospace;
            font-size: 11px;
        """)
        path_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(path_display)

        # Steps
        steps_label = QLabel(_('cert_manual_steps'))
        steps_label.setWordWrap(True)
        steps_label.setStyleSheet("background: white; padding: 15px; border-radius: 8px; border: 1px solid #ddd;")
        layout.addWidget(steps_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Open folder button
        self.open_folder_button = QPushButton(_('cert_open_folder'))
        self.open_folder_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.open_folder_button.clicked.connect(self.open_certificate_folder)

        # Completed button
        self.completed_button = QPushButton(_('cert_manual_complete'))
        self.completed_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.completed_button.clicked.connect(self.accept)

        # Cancel button
        cancel_button = QPushButton(_('cancel'))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.open_folder_button)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.completed_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def open_certificate_folder(self):
        """Open certificate folder in file explorer"""
        try:
            cert_dir = os.path.dirname(self.cert_path)
            if os.path.exists(cert_dir):
                if sys.platform == "win32":
                    subprocess.Popen(['explorer', cert_dir])
                elif sys.platform == "darwin":
                    subprocess.Popen(['open', cert_dir])
                else:
                    # Linux
                    subprocess.Popen(['xdg-open', cert_dir])
            else:
                QMessageBox.warning(self, _('error'), _('certificate_not_found'))
        except Exception as e:
            QMessageBox.warning(self, _('error'), _('file_open_error').format(str(e)))


class AddAccountDialog(QDialog):
    """Add account dialog
    
    Provides two methods to add accounts:
    1. Manual: Paste JSON data from browser
    2. Auto: Use Chrome extension (coming soon)
    """

    def __init__(self, parent=None):
        """Initialize add account dialog
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(_('add_account_title'))
        self.setGeometry(200, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # Tab widget
        self.tab_widget = QTabWidget()

        # Manual tab
        manual_tab = self.create_manual_tab()
        self.tab_widget.addTab(manual_tab, _('tab_manual'))

        # Auto tab
        auto_tab = self.create_auto_tab()
        self.tab_widget.addTab(auto_tab, _('tab_auto'))

        main_layout.addWidget(self.tab_widget)

        # Main buttons (common for both tabs)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        # Create account button (left side)
        self.create_account_button = QPushButton(_('create_account'))
        self.create_account_button.setMinimumHeight(28)
        self.create_account_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.create_account_button.clicked.connect(self.open_account_creation_page)

        self.add_button = QPushButton(_('add'))
        self.add_button.setMinimumHeight(28)
        self.add_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton(_('cancel'))
        self.cancel_button.setMinimumHeight(28)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.create_account_button)
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def create_manual_tab(self):
        """Create manual JSON addition tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Title
        title_label = QLabel(_('manual_method_title'))
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)

        # Main layout (left-right)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        # Left panel (form)
        left_panel = QVBoxLayout()
        left_panel.setSpacing(8)

        # Instruction
        instruction_label = QLabel(_('add_account_instruction'))
        instruction_label.setFont(QFont("Arial", 10))
        left_panel.addWidget(instruction_label)

        # Text edit
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(_('add_account_placeholder'))
        left_panel.addWidget(self.text_edit)

        # Info button
        self.info_button = QPushButton(_('how_to_get_json'))
        self.info_button.setMaximumWidth(220)
        self.info_button.clicked.connect(self.toggle_info_panel)
        left_panel.addWidget(self.info_button)

        content_layout.addLayout(left_panel, 1)

        # Right panel (info panel) - initially hidden
        self.info_panel = self.create_info_panel()
        self.info_panel.hide()
        self.info_panel_visible = False
        content_layout.addWidget(self.info_panel, 1)

        layout.addLayout(content_layout)
        tab_widget.setLayout(layout)
        return tab_widget

    def create_auto_tab(self):
        """Create Chrome extension auto-add tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Title
        title_label = QLabel(_('auto_method_title'))
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(12, 12, 12, 12)
        scroll_layout.setSpacing(16)

        # Chrome extension description
        chrome_title = QLabel(_('chrome_extension_title'))
        chrome_title.setFont(QFont("Arial", 11, QFont.Bold))
        scroll_layout.addWidget(chrome_title)

        chrome_desc = QLabel(_('chrome_extension_description'))
        chrome_desc.setWordWrap(True)
        chrome_desc.setStyleSheet("QLabel { color: #666; }")
        scroll_layout.addWidget(chrome_desc)

        # Steps
        steps_widget = QWidget()
        steps_widget.setStyleSheet("QWidget { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 12px; }")
        steps_layout = QVBoxLayout()
        steps_layout.setSpacing(8)

        steps = [
            _('chrome_extension_step_1'),
            _('chrome_extension_step_2'),
            _('chrome_extension_step_3'),
            _('chrome_extension_step_4')
        ]

        for step in steps:
            step_label = QLabel(step)
            step_label.setWordWrap(True)
            step_label.setStyleSheet("QLabel { margin: 4px 0; }")
            steps_layout.addWidget(step_label)

        steps_widget.setLayout(steps_layout)
        scroll_layout.addWidget(steps_widget)

        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)
        tab_widget.setLayout(layout)
        return tab_widget

    def create_info_panel(self):
        """Create info panel"""
        panel = QWidget()
        panel.setMaximumWidth(400)
        panel.setStyleSheet("QWidget { background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 8px; }")

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Title
        title = QLabel(_('json_info_title'))
        title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(title)

        # Steps
        steps_text = f"""
{_('step_1')}<br><br>
{_('step_2')}<br><br>
{_('step_3')}<br><br>
{_('step_4')}<br><br>
{_('step_5')}<br><br>
{_('step_6')}<br><br>
{_('step_7')}
        """

        steps_label = QLabel(steps_text)
        steps_label.setWordWrap(True)
        steps_label.setStyleSheet("QLabel { background: white; padding: 8px; border-radius: 4px; }")
        layout.addWidget(steps_label)

        # JavaScript code (hidden, only copy button)
        self.javascript_code = """(async () => {
  const request = indexedDB.open("firebaseLocalStorageDb");

  request.onsuccess = function (event) {
    const db = event.target.result;
    const tx = db.transaction("firebaseLocalStorage", "readonly");
    const store = tx.objectStore("firebaseLocalStorage");

    const getAllReq = store.getAll();

    getAllReq.onsuccess = function () {
      const results = getAllReq.result;

      // ilk kaydın value'sunu al
      const firstValue = results[0]?.value;
      console.log("Value (object):", firstValue);

      // JSON string'e çevir
      const valueString = JSON.stringify(firstValue, null, 2);

      // buton ekle
      const btn = document.createElement("button");
      btn.innerText = "-> Copy JSON <--";
      btn.style.position = "fixed";
      btn.style.top = "20px";
      btn.style.right = "20px";
      btn.style.zIndex = 9999;
      btn.onclick = () => {
        navigator.clipboard.writeText(valueString).then(() => {
          alert("Copied!");
        });
      };
      document.body.appendChild(btn);
    };
  };
})();"""

        # Copy code button
        self.copy_button = QPushButton(_('copy_javascript'))
        self.copy_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }")
        self.copy_button.clicked.connect(self.copy_javascript_code)
        layout.addWidget(self.copy_button)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def toggle_info_panel(self):
        """Toggle info panel visibility"""
        self.info_panel_visible = not self.info_panel_visible

        if self.info_panel_visible:
            self.info_panel.show()
            self.info_button.setText(_('how_to_get_json_close'))
            # Increase dialog width
            self.resize(1100, 500)
        else:
            self.info_panel.hide()
            self.info_button.setText(_('how_to_get_json'))
            # Restore dialog width
            self.resize(700, 500)

    def copy_javascript_code(self):
        """Copy JavaScript code to clipboard"""
        try:
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(self.javascript_code)

            # Temporarily change button text
            original_text = self.copy_button.text()
            self.copy_button.setText(_('copied'))

            # Revert after 2 seconds
            QTimer.singleShot(2000, lambda: self.copy_button.setText(original_text))

        except Exception as e:
            self.copy_button.setText(_('copy_error'))
            QTimer.singleShot(2000, lambda: self.copy_button.setText(_('copy_javascript')))

    def open_account_creation_page(self):
        """Open account creation page in browser"""
        webbrowser.open("https://app.warp.dev/login/")

    def get_json_data(self) -> str:
        """Get JSON data from text edit
        
        Returns:
            JSON string entered by user
        """
        return self.text_edit.toPlainText().strip()


class HelpDialog(QDialog):
    """Help and usage guide dialog
    
    Shows comprehensive help information about the application including:
    - What is Warp Account Manager
    - How it works
    - How to use
    """

    def __init__(self, parent=None):
        """Initialize help dialog
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(_('help_title'))
        self.setGeometry(250, 250, 700, 550)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel(_('help_title'))
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2196F3; margin-bottom: 15px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(20)

        # Section 1: What is it?
        section1 = self.create_section(
            _('help_what_is'),
            _('help_what_is_content')
        )
        content_layout.addWidget(section1)

        # Section 2: How does it work?
        section2 = self.create_section(
            _('help_how_works'),
            _('help_how_works_content')
        )
        content_layout.addWidget(section2)

        # Section 3: How to use?
        section3 = self.create_section(
            _('help_how_to_use'),
            _('help_how_to_use_content')
        )
        content_layout.addWidget(section3)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # Close button
        close_button = QPushButton(_('close'))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 30px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        close_button.clicked.connect(self.accept)

        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(close_button)
        close_layout.addStretch()
        layout.addLayout(close_layout)

        self.setLayout(layout)

    def create_section(self, title: str, content: str) -> QWidget:
        """Create a help section widget
        
        Args:
            title: Section title
            content: Section content
            
        Returns:
            QWidget with formatted section
        """
        section_widget = QWidget()
        section_widget.setStyleSheet("QWidget { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; }")

        section_layout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(10)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet("color: #333; margin-bottom: 5px;")
        section_layout.addWidget(title_label)

        # Content
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("color: #555; line-height: 1.4;")
        section_layout.addWidget(content_label)

        section_widget.setLayout(section_layout)
        return section_widget

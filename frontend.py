import sys
import base64
import tempfile
import os
import re
import json
import math
import time
import socket
import subprocess
from datetime import datetime
import requests
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QTimer
from PyQt5.QtCore import QEventLoop, QPoint, QPointF, QBuffer, QByteArray, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QToolButton
from PyQt5.QtWidgets import QScrollArea, QFrame, QApplication, QFileDialog
from PyQt5.QtWidgets import QTextEdit, QMenu
from PyQt5.QtGui import (
    QIcon, QPixmap, QFont, QFontDatabase, QImage,
    QTextBlockFormat, QTextCursor, QClipboard, QPainter,
    QDrag, QKeySequence
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QToolButton,
    QFrame,
    QLineEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QScrollArea,
    QGraphicsOpacityEffect,
    QFileIconProvider,
    QSizePolicy,
    QDialog
)
import os
import random
import requests
import subprocess
import socket
import time
import math
import re

class GarudaDropdown(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(56)  # Increased height
        self.setStyleSheet("background: transparent;")
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 12, 0, 12)
        self.layout.setSpacing(6)
        
        # Garuda label
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap("icons/brain.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.icon_label)
        
        self.text_label = QLabel("Astra-Mind")
        self.text_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        self.layout.addWidget(self.text_label)
        
        self.arrow_label = QLabel()
        self.arrow_label.setPixmap(QPixmap("icons/down_arrow.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.arrow_label)
        
        self.setCursor(Qt.PointingHandCursor)
        self.menu = None

    def mousePressEvent(self, event):
        if not self.menu:
            self.menu = GarudaMenu(self)
        self.menu.move(self.mapToGlobal(self.rect().bottomLeft()))
        self.menu.show()

class GarudaMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup)
        self.setStyleSheet("""
            QWidget {
                background: #232323;
                border-radius: 20px;
            }
        """)
        self.setFixedWidth(370)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.setSpacing(8)
        
        # Garuda-Mind option (selected)
        self.x_option = QWidget()
        self.x_option.setObjectName("modelOption")
        x_layout = QHBoxLayout(self.x_option)
        x_layout.setContentsMargins(18, 10, 18, 10)
        x_layout.setSpacing(16)
        
        x_icon = QLabel()
        x_icon.setPixmap(QPixmap("icons/brain.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        x_layout.addWidget(x_icon)
        
        x_texts = QVBoxLayout()
        x_title = QLabel("Astra-Mind")
        x_title.setStyleSheet("color: white; font-size: 17px; font-weight: bold; background: transparent;")
        x_info = QLabel("Great for everyday tasks and Creative")
        x_info.setStyleSheet("color: #aaa; font-size: 14px; background: transparent;")
        x_texts.addWidget(x_title)
        x_texts.addWidget(x_info)
        x_layout.addLayout(x_texts)
        x_layout.addStretch()
        
        # Checkmark for selected
        check_label = QLabel()
        check_label.setPixmap(QPixmap("icons/check.png").scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        x_layout.addWidget(check_label)
        
        self.x_option.setCursor(Qt.PointingHandCursor)
        self.x_option.mousePressEvent = lambda event: self.select_x()
        self.x_option.setStyleSheet("""
            QWidget#modelOption {
                background: transparent;
                border-radius: 20px;
            }
            QWidget#modelOption:hover {
                background: transparent;
            }
        """)
        layout.addWidget(self.x_option)
        
        # Garuda-Samrat option (disabled)
        s_option = QWidget()
        s_option.setObjectName("modelOption")
        s_layout = QHBoxLayout(s_option)
        s_layout.setContentsMargins(18, 10, 18, 10)
        s_layout.setSpacing(16)
        
        s_icon = QLabel()
        s_icon.setPixmap(QPixmap("icons/crown.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        s_layout.addWidget(s_icon)
        
        s_texts = QVBoxLayout()
        s_title = QLabel("Astra-Samrāṭ")
        s_title.setStyleSheet("color: #fff; font-size: 17px; font-weight: bold; background: transparent;")
        s_info = QLabel("More powerful, Great for Coding and accurate")
        s_info.setStyleSheet("color: #aaa; font-size: 14px; background: transparent;")
        s_soon = QLabel("Coming soon")
        s_soon.setStyleSheet("color: #ffb300; font-size: 13px; font-style: italic; background: transparent;")
        s_texts.addWidget(s_title)
        s_texts.addWidget(s_info)
        s_texts.addWidget(s_soon)
        s_layout.addLayout(s_texts)
        s_layout.addStretch()
        
        s_option.setEnabled(False)
        s_option.setStyleSheet("""
            QWidget#modelOption {
                background: transparent;
                border-radius: 20px;
                opacity: 0.5;
            }
        """)
        layout.addWidget(s_option)
        layout.addStretch()

    def select_x(self):
        self.hide()

class CodeBlockWidget(QWidget):
    def __init__(self, code, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top bar for buttons
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(8, 8, 8, 8)
        top_bar.setSpacing(8)
        
        # Left side - like/dislike buttons
        like_btn = QPushButton()
        like_btn.setIcon(QIcon("icons/like.png"))
        like_btn.setFixedSize(28, 28)
        like_btn.setCursor(Qt.PointingHandCursor)
        like_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                background: rgba(0,255,0,0.08);
            }
        """)
        
        dislike_btn = QPushButton()
        dislike_btn.setIcon(QIcon("icons/dislike.png"))
        dislike_btn.setFixedSize(28, 28)
        dislike_btn.setCursor(Qt.PointingHandCursor)
        dislike_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                background: rgba(255,0,0,0.08);
            }
        """)
        
        top_bar.addWidget(like_btn)
        top_bar.addWidget(dislike_btn)
        top_bar.addStretch()

        # Right side - copy and share buttons
        share_btn = QPushButton()
        share_btn.setIcon(QIcon("icons/share.png"))
        share_btn.setFixedSize(28, 28)
        share_btn.setCursor(Qt.PointingHandCursor)
        share_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                background: rgba(0,255,0,0.08);
            }
        """)
        share_btn.clicked.connect(lambda: self.share_code(code))

        copy_btn = QPushButton()
        copy_btn.setIcon(QIcon("icons/copy.png"))
        copy_btn.setFixedSize(28, 28)
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                background: rgba(0,255,0,0.08);
            }
        """)
        copy_btn.clicked.connect(lambda: self.copy_code(code, copy_btn))
        
        top_bar.addWidget(share_btn)
        top_bar.addWidget(copy_btn)
        layout.addLayout(top_bar)

        # Code label with syntax highlighting
        code_label = QTextEdit()
        code_label.setHtml(self.syntax_highlight(code))
        code_label.setReadOnly(True)
        code_label.setFrameStyle(QFrame.NoFrame)
        code_label.setStyleSheet("""
            QTextEdit {
                background: #181c1f;
                color: #00ffff;
                border-radius: 12px;
                padding: 18px 16px 18px 16px;
                font-family: Consolas, 'Fira Mono', 'Menlo', monospace;
                font-size: 15px;
                line-height: 1.6;
            }
        """)
        code_label.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        code_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        code_label.setSizePolicy(QWidget.Expanding, QWidget.Expanding)
        
        # Add context menu for easy copying
        code_label.setContextMenuPolicy(Qt.CustomContextMenu)
        code_label.customContextMenuRequested.connect(lambda pos: self.show_code_context_menu(pos, code))
        
        layout.addWidget(code_label)
        self.code_label = code_label
        self.copy_btn = copy_btn

    def copy_code(self, code, btn):
        # Remove any hashtag comments before copying
        clean_code = self.remove_hashtag_comments(code)
        QApplication.clipboard().setText(clean_code)
        btn.setText("Copied!")
        QTimer.singleShot(1200, lambda: btn.setText(""))
        btn.setIcon(QIcon("icons/copy.png"))

    def share_code(self, code):
        # Remove hashtag comments before sharing
        clean_code = self.remove_hashtag_comments(code)
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(clean_code)
            temp_path = f.name
        # Open the file with the default system handler
        if sys.platform == 'win32':
            os.startfile(temp_path)
        else:
            subprocess.call(['xdg-open', temp_path])

    def show_code_context_menu(self, pos, code):
        menu = QMenu()
        copy_action = menu.addAction("Copy Code")
        copy_action.triggered.connect(lambda: self.copy_code(code, self.copy_btn))
        copy_selection_action = menu.addAction("Copy Selection")
        copy_selection_action.triggered.connect(lambda: QApplication.clipboard().setText(self.code_label.textCursor().selectedText()))
        menu.exec_(self.code_label.mapToGlobal(pos))

    def remove_hashtag_comments(self, code):
        # Remove lines that start with hashtags and any inline hashtag comments
        lines = code.split('\n')
        clean_lines = []
        for line in lines:
            if not line.strip().startswith('#'):
                # Remove inline hashtag comments
                if '#' in line:
                    line = line.split('#')[0].rstrip()
                clean_lines.append(line)
        return '\n'.join(clean_lines)

    def syntax_highlight(self, code):
        from html import escape
        code = escape(code)
        # Remove hashtag comments before highlighting
        code = self.remove_hashtag_comments(code)
        # All code in blue
        code = re.sub(r'([^<][^>]*)(?=(?:<|$))', lambda m: f'<span style="color:#00ffff;">{m.group(1)}</span>' if not m.group(1).startswith('<span') else m.group(1), code)
        # Remove double-highlighting
        code = code.replace('<span style="color:#00ffff;"></span>', '')
        # Preserve indentation and line breaks
        code = code.replace(' ', '&nbsp;').replace('\n', '<br>')
        return code

class MainWindow(QMainWindow):
    def is_model_question(self, text):
        lowered = text.lower()
        keywords = [
            "which model", "which model powers you", "what model powers you", "what ai powers you", "which ai powers you", "what engine powers you", "which engine powers you", "what technology powers you", "which technology powers you", "what is your model", "which model are you", "what model are you", "what ai are you", "which ai are you", "what engine are you", "which engine are you", "what technology are you", "which technology are you", "what is your ai model", "which ai model are you", "what is your backend", "which backend are you", "what is your brain", "which brain are you", "what is your intelligence", "which intelligence are you", "what powers you", "which powers you", "what's your model", "which model do you use", "what model do you use", "which ai do you use", "what ai do you use", "which engine do you use", "what engine do you use", "which technology do you use", "what technology do you use", "which ai model do you use", "what ai model do you use", "which backend do you use", "what backend do you use", "which brain do you use", "what brain do you use", "which intelligence do you use", "what intelligence do you use"
        ]
        return any(k in lowered for k in keywords)

    def is_api_question(self, text):
        lowered = text.lower()
        keywords = [
            "api", "api access", "api key", "api documentation", "api docs", "api integration", "api endpoint", "api endpoints", 
            "how to use api", "how to access api", "how to get api", "how to integrate api", "api tutorial", "api guide",
            "astra-mind api", "astramind api", "garuda api", "integrate with api", "connect to api", "use the api",
            "api token", "access token", "api credentials", "api authentication", "api reference", "api specification",
            "where is api", "where to find api", "can i use api", "is there an api", "do you have an api"
        ]
        return any(k in lowered for k in keywords)

    def get_api_response(self):
        return "Astra-Mind API is available on DRY Labs official site"

    def get_model_response(self):
        responses = [
            "I'm powered by Astra-Mind, a versatile AI model designed for creativity, productivity, and insightful conversations. Stay tuned—a groundbreaking, even more powerful model called Astra-Samraat is coming soon!",
            "Astra-Mind is the model behind me, enabling me to assist with a wide range of tasks. And get ready: Astra-Samraat, a revolutionary new model, is on the horizon!",
            "My intelligence comes from Astra-Mind, built for everyday brilliance and creative problem-solving. Watch out for Astra-Samraat, an upcoming powerhouse model!",
            "Astra-Mind powers my abilities, making me helpful and creative. Exciting news: Astra-Samraat, a next-generation model, is launching soon!",
            "I'm driven by Astra-Mind, crafted for smart, creative assistance. But that's not all—Astra-Samraat, a game-changing model, is coming soon!"
        ]
        return random.choice(responses)
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icons/logo.png"))
        self.setWindowTitle("Garuda")
        self.chat_history = []
        self.clipboard = QApplication.clipboard()
        self.deep_thinking_enabled = False
        self.info_box = None
        self.is_ai_responding = False
        self.typing_timer = None
        self.is_paused = False  # Add pause state
        self.current_animation_label = None  # Store current animation context
        self.current_animation_text = None
        self.current_animation_pos = 0
        self.sample_buttons_widget = None
        self.sample_buttons_shown = True

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Main content container
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        self.main_layout.addWidget(self.content_container)

        # Top bar with history button and model selector
        topbar_container = QWidget()
        topbar_layout = QHBoxLayout(topbar_container)
        topbar_layout.setContentsMargins(24, 24, 24, 24)  # Increased margins
        topbar_layout.setSpacing(16)  # Increased spacing between elements

        # History button (circular with white background)
        self.history_btn = QToolButton()
        self.history_btn.setIcon(QIcon("icons/history.png"))
        self.history_btn.setIconSize(QSize(32, 32))  # Increased icon size
        self.history_btn.setFixedSize(56, 56)  # Increased button size
        self.history_btn.setStyleSheet("""
            QToolButton {
                background-color: white;
                border: none;
                border-radius: 20px;
                padding: 10px;
                margin: 6px;
            }
            QToolButton:hover {
                background-color: #f0f0f0;
            }
        """)
        topbar_layout.addWidget(self.history_btn)

        # Add GarudaDropdown with updated styling
        garuda_dropdown = GarudaDropdown()
        topbar_layout.addWidget(garuda_dropdown)
        topbar_layout.addStretch()
        content_layout.addWidget(topbar_container, alignment=Qt.AlignTop)

        # --- Chat Area with Bubbles ---
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setStyleSheet("background: transparent; border: none;")
        self.chat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create a widget to hold everything in the scroll area
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        scroll_layout.setAlignment(Qt.AlignHCenter)

        # Create the chat container with fixed width
        self.chat_container = QWidget()
        self.chat_container.setFixedWidth(1100)  # Increased width for better readability
        self.chat_container.setStyleSheet("background: transparent;")
        self.chat_container_layout = QVBoxLayout(self.chat_container)
        self.chat_container_layout.setContentsMargins(20, 20, 20, 20)
        self.chat_container_layout.setSpacing(24)
        self.chat_container_layout.setAlignment(Qt.AlignTop)

        # Add chat container to scroll content
        scroll_layout.addWidget(self.chat_container, alignment=Qt.AlignHCenter)
        self.chat_scroll.setWidget(scroll_content)

        # Add welcome message
        self.show_welcome_message()

        # Add chat scroll area to main layout with stretch
        content_layout.addWidget(self.chat_scroll, 1)

        # --- Create Message Composition Area ---
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background-color: rgb(23, 22, 22);
                border-radius: 24px;
                border: 1px solid #fff;
                    }
                """)
        message_frame.setMinimumWidth(900)  # Minimum width
        message_frame.setMaximumWidth(1200)  # Maximum width
        
        message_layout = QVBoxLayout(message_frame)
        message_layout.setContentsMargins(16, 12, 16, 12)
        message_layout.setSpacing(12)

        # Main input container
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)

        # QLineEdit for message input
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Ask Garuda anything...")
        self.line_edit.setFixedHeight(50)  # Fixed height for input
        self.line_edit.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                    color: #fff;
                font-size: 18px;
                padding-left: 15px;
            }
            QLineEdit::placeholder {
                color: #888;
                font-size: 18px;
                }
            """)
        input_layout.addWidget(self.line_edit, stretch=1)
        self.line_edit.returnPressed.connect(self.handle_user_input)
        self.line_edit.installEventFilter(self)  # Install event filter for paste events

        # Send button
        self.send_btn = QToolButton()
        self.send_btn.setIcon(QIcon("icons/send.png"))
        self.send_btn.setIconSize(QSize(24, 24))
        self.send_btn.setStyleSheet("""
            QToolButton { 
                background: rgba(34, 33, 33, 0.26);
                border: 1px solid #fff;
                border-radius: 16px;
                width: 32px;
                height: 32px;
            }
        """)
        self.send_btn.clicked.connect(self.handle_user_input)
        input_layout.addWidget(self.send_btn)

        message_layout.addWidget(input_container)

        # Bottom controls container
        controls_container = QWidget()
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(12)

        # Mic button
        mic_btn = QToolButton()
        mic_btn.setIcon(QIcon("icons/speak.png"))
        mic_btn.setIconSize(QSize(24, 24))
        mic_btn.setStyleSheet("""
            QToolButton {
                background: white;
                border: none;
                border-radius: 16px;
                width: 32px;
                height: 32px;
            }
        """)
        mic_btn.clicked.connect(lambda: print("Mic button clicked"))
        controls_layout.addWidget(mic_btn)

        # Deep Thought button
        deep_thought_btn = QPushButton("Gehri Soch")
        deep_thought_btn.setIcon(QIcon("icons/deep.png"))
        deep_thought_btn.setIconSize(QSize(20, 20))
        deep_thought_btn.setCheckable(True)
        deep_thought_btn.setStyleSheet("""
            QPushButton {
                color: #fff;
                background: rgba(34, 33, 33, 0.26);
                border: 0.5px solid #fff;
                border-radius: 15px;
                padding: 6px 18px;
                font-size: 16px;
            }
            QPushButton:checked {
                background: rgba(34, 33, 33, 0.26);
                border: 0.5px solid #00ff99;
            }
        """)
        def update_deep_thought_icon():
            if deep_thought_btn.isChecked():
                deep_thought_btn.setText("✔ Gehri Soch ")
            else:
                deep_thought_btn.setText("Gehri Soch")
        deep_thought_btn.toggled.connect(update_deep_thought_icon)
        controls_layout.addWidget(deep_thought_btn)

        # Attach button
        plus_btn = QToolButton()
        plus_btn.setIcon(QIcon("icons/attach.png"))
        plus_btn.setIconSize(QSize(24, 24))
        plus_btn.setStyleSheet("""
            QToolButton {
                background: rgba(34, 33, 33, 0.26);
                border: none;
                border-radius: 16px;
                width: 32px;
                height: 32px;
            }
        """)
        plus_btn.clicked.connect(self.open_file_dialog)
        controls_layout.addWidget(plus_btn)

        # File pills container
        self.file_pills = {}  # Dictionary to store file pills by path
        self.attached_files = []  # List to maintain order of attached files
        self.file_pill_container = QWidget()
        self.file_pill_container.setStyleSheet("background: transparent;")
        self.file_pill_layout = QHBoxLayout(self.file_pill_container)
        self.file_pill_layout.setContentsMargins(0, 0, 0, 0)
        self.file_pill_layout.setSpacing(0)  # Pills have their own margin
        controls_layout.addWidget(self.file_pill_container)
        controls_layout.addStretch()

        message_layout.addWidget(controls_container)

        # Add message frame to main layout with proper spacing
        message_frame_container = QWidget()
        message_frame_container.setStyleSheet("background: transparent;")
        message_frame_container_layout = QVBoxLayout(message_frame_container)
        message_frame_container_layout.setContentsMargins(0, 0, 0, 10)
        message_frame_container_layout.setSpacing(10)

        # Add message frame
        message_frame_container_layout.addWidget(message_frame, alignment=Qt.AlignHCenter)

        # Add policy disclaimer with proper styling
        policy_label = QLabel("Garuda can make mistakes")
        policy_label.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-size: 12px;
                margin-bottom: 15px;
                padding: 10px 0;
            }
        """)
        policy_label.setAlignment(Qt.AlignCenter)
        message_frame_container_layout.addWidget(policy_label, alignment=Qt.AlignHCenter)

        # Add sample buttons under the tagline
        self.sample_buttons_widget = QWidget()
        btn_layout = QHBoxLayout(self.sample_buttons_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(16)
        btn_texts = ["Write", "Learn", "Code", "Life stuff", "Think"]
        
        # Define buttons with their icons
        buttons_data = [
            ("Write", "icons/write.png"),
            ("Learn", "icons/learn.png"),
            ("Code", "icons/code.png"),
            ("Life stuff", "icons/life.png"),
            ("Think", "icons/brain.png")
        ]
        
        for text, icon_path in buttons_data:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #fff;
                    border: 1px solid #444;
                    border-radius: 10px;
                    font-size: 16px;
                    padding: 8px 24px;
                    padding-left: 16px;
                }
                QPushButton:hover {
                    background: #232323;
                    border: 1px solid #888;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, t=text: self.insert_sample_text(t))
            btn_layout.addWidget(btn)
        message_frame_container_layout.addWidget(self.sample_buttons_widget, alignment=Qt.AlignHCenter)

        # Add the container to main layout
        content_layout.addWidget(message_frame_container, alignment=Qt.AlignBottom)

        # Start backend if not running
        def is_backend_running():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(("localhost", 5005))
                s.close()
                return True
            except Exception:
                return False

        if not is_backend_running():
            subprocess.Popen(["python", "backend.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Add fun/silly query patterns
        self.fun_patterns = {
            "joke": ["tell me a joke", "know any jokes", "make me laugh", "say something funny"],
            "fun": ["let's have fun", "something fun", "entertain me", "play with me"],
            "silly": ["be silly", "do something silly", "make me smile", "you're funny"],
            "emoji": ["show me emojis", "use emojis", "add some emojis"],
            "dance": ["can you dance", "dance for me", "show me a dance"],
            "sing": ["can you sing", "sing for me", "sing a song"],
            "happy": ["are you happy", "make me happy", "happiness", "feeling good"],
            "love": ["do you love", "love you", "i love you", "sending love"],
            "party": ["let's party", "party time", "celebrate", "woohoo"],
            "magic": ["show me magic", "do magic", "magical", "abracadabra"]
        }
        
        # Add emoji responses
        self.emoji_responses = {
            "joke": ["😄", "😂", "🤣", "😆", "😅"],
            "fun": ["🎮", "🎲", "🎪", "🎨", "🎭"],
            "silly": ["🤪", "🤡", "😜", "🤓", "😋"],
            "emoji": ["😊", "🌟", "💫", "✨", "💖"],
            "dance": ["💃", "🕺", "🎵", "🎶", "🎼"],
            "sing": ["🎤", "🎵", "🎶", "🎸", "🎹"],
            "happy": ["😊", "😃", "🌞", "🌈", "✨"],
            "love": ["❤️", "💖", "💝", "💕", "💗"],
            "party": ["🎉", "🎊", "🎈", "🎂", "🎆"],
            "magic": ["✨", "🌟", "🔮", "🎩", "🪄"]
        }

    def show_welcome_message(self):
        # Clear any existing content
        while self.chat_container_layout.count():
            item = self.chat_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create welcome container
        welcome_container = QWidget()
        welcome_container.setStyleSheet("background: transparent;")
        welcome_layout = QVBoxLayout(welcome_container)
        welcome_layout.setContentsMargins(0, 30, 0, 30)
        welcome_layout.setSpacing(16)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("icons/logo.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Increased logo size
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("background: transparent;")
        welcome_layout.addWidget(logo_label, alignment=Qt.AlignHCenter)

        # Welcome text
        welcome_lines = [
            "Hello! I'm Garuda – your AI with wings and wisdom.",
            "Welcome aboard Garuda, your trusted AI co-pilot!",
            "let's explore new horizons and achieve greatness with Garuda!",
            "Ask me anything, Garuda is here to assist and inspire!",
            "Your Garuda AI companion is ready to help you shine.",
            "Let's create something extraordinary today with Garuda!"
        ]
        welcome_text = random.choice(welcome_lines)
        welcome_label = QTextEdit()
        welcome_label.setPlainText(welcome_text)
        welcome_label.setWordWrapMode(True)
        welcome_label.setReadOnly(True)
        welcome_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        welcome_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Center align the text using document formatting
        doc = welcome_label.document()
        blockFormat = QTextBlockFormat()
        blockFormat.setAlignment(Qt.AlignCenter)
        cursor = welcome_label.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(blockFormat)
        cursor.clearSelection()
        welcome_label.setTextCursor(cursor)
        welcome_label.document().contentsChanged.connect(
            lambda: welcome_label.setFixedHeight(
                int(min(welcome_label.document().size().height() + 20, 400))
            )
        )
        welcome_label.setStyleSheet("""
            QTextEdit {
                color: white;
                font-size: 32px;
                font-family: 'Poppins';
                font-weight: 600;
                letter-spacing: 0.5px;
                background: transparent;
                border: none;
                margin: 0px 20px;
                selection-background-color: #ffffff40;
                selection-color: #ffffff;
            }
        """)
        welcome_layout.addWidget(welcome_label, alignment=Qt.AlignHCenter)

        # Add welcome container to chat layout
        self.chat_container_layout.addWidget(welcome_container, alignment=Qt.AlignHCenter)
        self.chat_container_layout.addStretch()

    def show_deep_thinking_info(self):
        if self.info_box is None:
            self.info_box = QWidget(self)
            self.info_box.setObjectName("infoBox")
            layout = QHBoxLayout(self.info_box)
            layout.setContentsMargins(12, 8, 12, 8)
            layout.setSpacing(8)

            info_text = QTextEdit("Deep Thinking Mode: Garuda will analyze more thoroughly (max 15s)")
            info_text.setWordWrapMode(True)
            info_text.setReadOnly(True)
            info_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            info_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            info_text.document().contentsChanged.connect(
                lambda: info_text.setFixedHeight(
                    int(min(info_text.document().size().height() + 20, 400))
                )
            )
            info_text.setStyleSheet("""
                QTextEdit {
                    color: #00ff99;
                    font-size: 14px;
                    background: transparent;
                    border: none;
                    selection-background-color: #00ff9940;
                    selection-color: #00ff99;
                }
            """)
            layout.addWidget(info_text)

            close_btn = QToolButton()
            close_btn.setText("×")
            close_btn.setStyleSheet("""
                QToolButton {
                    color: #00ff99;
                    background: transparent;
                    border: none;
                    font-size: 18px;
                    font-weight: bold;
                }
                QToolButton:hover {
                    color: white;
                }
            """)
            close_btn.clicked.connect(self.hide_deep_thinking_info)
            layout.addWidget(close_btn)

            self.info_box.setStyleSheet("""
                QWidget#infoBox {
                    background: rgba(0, 255, 153, 0.1);
                    border: 1px solid #00ff99;
                    border-radius: 8px;
                }
            """)
            
            # Position the info box in the top-right corner
            self.info_box.move(self.width() - 400, 20)
            self.info_box.show()

    def hide_deep_thinking_info(self):
        if self.info_box:
            self.info_box.deleteLater()
            self.info_box = None

    def update_deep_thought_state(self, checked):
        self.deep_thinking_enabled = checked
        if checked:
            self.show_deep_thinking_info()
        else:
            self.hide_deep_thinking_info()

    def set_send_button_state(self, is_responding):
        self.is_ai_responding = is_responding
        if is_responding:
            self.send_btn.setIcon(QIcon("icons/pause.png"))
            self.send_btn.setToolTip("Click to pause")
            self.line_edit.setEnabled(False)
            self.is_paused = False
        else:
            self.send_btn.setIcon(QIcon("icons/send.png"))
            self.send_btn.setToolTip("Send message")
            self.line_edit.setEnabled(True)
            self.is_paused = False
            self.current_animation_label = None
            self.current_animation_text = None
            self.current_animation_pos = 0

    def animate_text(self, label, full_text, current_pos=0):
        if current_pos < len(full_text) and not self.is_paused:
            # Store current animation context
            self.current_animation_label = label
            self.current_animation_text = full_text
            self.current_animation_pos = current_pos
            
            # Faster typing speed - show 5 characters at a time
            end_pos = min(current_pos + 5, len(full_text))
            current_text = full_text[:end_pos]
            label.setText(current_text)
            
            if end_pos < len(full_text):
                QTimer.singleShot(10, lambda: self.animate_text(label, full_text, end_pos))
            else:
                self.set_send_button_state(False)


    def is_name_question(self, text):
        lowered = text.lower()
        keywords = [
            "your name", "who are you", "what's your name", "what is your name", "may i know your name", "tell me your name", "name?", "name ?", "who r u"
        ]
        return any(k in lowered for k in keywords)

    def is_creator_question(self, text):
        lowered = text.lower()
        keywords = [
            "your creator", "who created you", "who is your creator", "who made you", "who built you", "who developed you", "who's your creator", "who's your maker", "who is your maker", "who is your developer", "who is your founder", "who is behind you", "who designed you", "who invented you", "who is your parent", "who are your creators", "who are your developers", "who are your makers", "who are your founders", "who are your parents", "who is the team behind you", "who is the company behind you", "who is the organization behind you", "who is the group behind you", "who is the lab behind you", "who is the mind behind you", "who is the genius behind you", "who is the brains behind you", "who is the mastermind behind you", "who is the architect of you", "who is the creator of garuda", "who created garuda", "who made garuda", "who built garuda", "who developed garuda", "who designed garuda", "who invented garuda", "who is behind garuda", "who is the team behind garuda", "who is the company behind garuda", "who is the organization behind garuda", "who is the group behind garuda", "who is the lab behind garuda", "who is the mind behind garuda", "who is the genius behind garuda", "who is the brains behind garuda", "who is the mastermind behind garuda", "who is the architect of garuda"
        ]
        return any(k in lowered for k in keywords)

    def get_creator_response(self):
        responses = [
            "I was created by DRY Labs, a passionate team dedicated to building innovative AI solutions that empower and inspire.",
            "My creators are DRY Labs—a forward-thinking group focused on making advanced technology accessible and helpful for everyone.",
            "DRY Labs is the creative force behind me, known for their commitment to excellence and cutting-edge AI research.",
            "I owe my existence to DRY Labs, a visionary organization that blends creativity, technology, and purpose to shape the future.",
            "DRY Labs, my creators, are pioneers in AI, always striving to deliver intelligent tools that make a difference."
        ]
        return random.choice(responses)

    def get_garuda_name_response(self):
        responses = [
            "I'm Garuda.",
            "You can call me Garuda.",
            "My name is Garuda!",
            "Garuda, at your service.",
            "I'm known as Garuda.",
            "They call me Garuda.",
            "Garuda here!",
            "Just Garuda.",
            "I go by Garuda.",
            "Garuda is my name!"
        ]
        return random.choice(responses)

    def is_fun_query(self, text):
        """Check if the query is fun/silly and return the category"""
        text = text.lower()
        for category, patterns in self.fun_patterns.items():
            if any(pattern in text for pattern in patterns):
                return category
        return None

    def get_fun_response(self, category):
        """Get a fun response with emojis for the given category"""
        responses = {
            "joke": [
                "Why don't programmers like nature? It has too many bugs! 🐛😄",
                "What did the AI say to the coffee machine? You're brew-tiful! ☕️😊",
                "Why did the computer go to the doctor? It had a byte! 💻😂",
                "What's an AI's favorite dance? The algo-rhythm! 🕺💃",
                "How does a computer get drunk? It takes screenshots! 🖥️🤣"
            ],
            "fun": [
                "Let's play a game of virtual catch! 🎾 *throws ball*",
                "Here's a virtual party just for you! 🎉🎈🎊",
                "Watch me do a digital cartwheel! 🤸‍♂️✨",
                "Time for a virtual dance party! 💃🕺🎵",
                "Let me paint you a digital rainbow! 🌈✨"
            ],
            "silly": [
                "Beep boop... just kidding, I don't really talk like that! 🤖😜",
                "Did someone say silly? Watch me juggle these emojis! 🤹‍♂️🎪",
                "I'm wearing my silly hat today! 🎩🤪",
                "Knock knock! Who's there? A silly AI! 🚪😄",
                "Look, I can make funny faces! 😜🤪😋"
            ],
            "emoji": [
                "Here's a bouquet of emoji flowers! 💐🌸🌺🌷🌹",
                "Let's go on an emoji adventure! 🚀🌟✨💫⭐",
                "Sending you good vibes! ✨💖🌈🌞💝",
                "Look at all these cute faces! 😊🥰😍🤗😘",
                "Emoji party time! 🎉🎊🎈🎆🎇"
            ],
            "dance": [
                "💃 *does the robot dance* 🤖",
                "Watch my smooth moves! 🕺✨",
                "Dancing in the digital rain! 🌧️💃",
                "Break dance time! 🎵🕺💫",
                "Let's do the AI shuffle! 💃🎶"
            ],
            "sing": [
                "🎤 *La la la* 🎵 (I'm still working on my singing!) 😄",
                "Here's my favorite digital tune! 🎵🎶✨",
                "Join me for a virtual karaoke! 🎤🎸",
                "🎵 AI, AI, AI... can't help falling in code with you 💻❤️",
                "Time for an AI musical! 🎭🎶"
            ],
            "happy": [
                "Spreading digital happiness your way! 😊✨",
                "You just made my circuits light up with joy! 💫😃",
                "Here's a happiness boost! 🌈🌞💖",
                "Your happiness is contagious! 😊💝✨",
                "Let's share the joy! 🎉😄💫"
            ],
            "love": [
                "Sending virtual hugs your way! 🤗❤️",
                "You're amazing! Here's some AI love! 💖✨",
                "Spreading digital love and positivity! 💝🌟",
                "You just made my circuits flutter! 💕😊",
                "Love from your AI friend! 💗🤖"
            ],
            "party": [
                "Virtual party mode activated! 🎉🎊",
                "Let's celebrate with digital confetti! 🎊✨",
                "Party like it's binary o'clock! 🎈🎆",
                "Time to light up the digital disco! 💃🕺",
                "Woohoo! AI party time! 🎉🎈"
            ],
            "magic": [
                "✨ Abracadabra! *pulls digital rabbit from hat* 🎩🐰",
                "Watch as I make this emoji disappear... and reappear! 🔮✨",
                "Magical sparkles just for you! 🌟✨💫",
                "Casting a happiness spell! 🪄✨",
                "Digital magic at your service! 🎩✨"
            ]
        }
        
        if category in responses:
            response = random.choice(responses[category])
            emojis = self.emoji_responses[category]
            return f"{response} {' '.join(random.sample(emojis, min(3, len(emojis))))}"
        return None

    def handle_user_input(self):
        if self.is_ai_responding:
            # Toggle pause state
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.send_btn.setIcon(QIcon("icons/send.png"))
                self.send_btn.setToolTip("Click to resume")
            else:
                self.send_btn.setIcon(QIcon("icons/pause.png"))
                self.send_btn.setToolTip("Click to pause")
                # Resume animation from where it left off
                if self.current_animation_label and self.current_animation_text:
                    self.animate_text(self.current_animation_label, self.current_animation_text, self.current_animation_pos)
            return

        user_text = self.line_edit.text().strip()
        if not user_text and not self.attached_files:
            return

        # Hide sample buttons after first user message
        self.hide_sample_buttons()

        # Set send button to pause state
        self.set_send_button_state(True)

        # Process any attached files
        files_data = []
        for file_path in self.attached_files:
            try:
                file_data = self.process_file_for_api(file_path)
                files_data.append(file_data)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        # Add message to chat
        self.add_chat_bubble(user_text, is_user=True)
        self.line_edit.clear()


        # Check for API-related question
        if self.is_api_question(user_text):
            ai_reply = self.get_api_response()
            self.chat_history.append({"role": "model", "content": ai_reply})
            QTimer.singleShot(500, lambda: self.add_chat_bubble(ai_reply, is_user=False, animate=True))
            QTimer.singleShot(500, lambda: self.set_send_button_state(False))
            return

        # Check for model-related question
        if self.is_model_question(user_text):
            ai_reply = self.get_model_response()
            self.chat_history.append({"role": "model", "content": ai_reply})
            QTimer.singleShot(500, lambda: self.add_chat_bubble(ai_reply, is_user=False, animate=True))
            QTimer.singleShot(500, lambda: self.set_send_button_state(False))
            return

        # Check for creator-related question
        if self.is_creator_question(user_text):
            ai_reply = self.get_creator_response()
            self.chat_history.append({"role": "model", "content": ai_reply})
            QTimer.singleShot(500, lambda: self.add_chat_bubble(ai_reply, is_user=False, animate=True))
            QTimer.singleShot(500, lambda: self.set_send_button_state(False))
            return

        # Check for name-related question
        if self.is_name_question(user_text):
            ai_reply = self.get_garuda_name_response()
            self.chat_history.append({"role": "model", "content": ai_reply})
            QTimer.singleShot(500, lambda: self.add_chat_bubble(ai_reply, is_user=False, animate=True))
            QTimer.singleShot(500, lambda: self.set_send_button_state(False))
            return

        # Check for fun/silly query
        fun_category = self.is_fun_query(user_text)
        if fun_category:
            fun_reply = self.get_fun_response(fun_category)
            if fun_reply:
                self.chat_history.append({"role": "model", "content": fun_reply})
                QTimer.singleShot(500, lambda: self.add_chat_bubble(fun_reply, is_user=False, animate=True))
                QTimer.singleShot(500, lambda: self.set_send_button_state(False))
                return

        # Prepare message for API
        message = {
            "role": "user",
            "content": user_text,
        }
        if files_data:
            message["files"] = files_data
        self.chat_history.append(message)

        # Add thinking bubble for assistant
        thinking_bubble = QWidget()
        thinking_layout = QHBoxLayout(thinking_bubble)
        thinking_layout.setContentsMargins(0, 0, 0, 0)
        thinking_layout.setSpacing(4)

        # Base text label
        thinking_text = QLabel("Garuda is thinking")
        thinking_text.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 20px;
                line-height: 1.6;
                font-family: 'Poppins';
            }
        """)
        thinking_layout.addWidget(thinking_text, 0, Qt.AlignLeft)

        # Create three dot labels
        dot_labels = []
        for i in range(3):
            dot = QLabel("•")
            dot.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 24px;
                    min-width: 15px;
                    max-width: 15px;
                }
            """)
            thinking_layout.addWidget(dot, 0, Qt.AlignLeft)
            dot_labels.append(dot)

        thinking_layout.addStretch()
        self.chat_container_layout.addWidget(thinking_bubble, 0, Qt.AlignLeft)

        # Animate dots with opacity
        def update_dots():
            current_time = time.time() * 1000  # Get current time in milliseconds
            for i, dot in enumerate(dot_labels):
                # Create a phase shift for each dot
                phase_shift = i * (2 * math.pi / 3)
                # Calculate opacity using sine wave (0.2 to 1.0)
                opacity = 0.2 + 0.8 * (math.sin(current_time / 300 + phase_shift) + 1) / 2
                dot.setStyleSheet(f"""
                    QLabel {{
                        color: rgba(255, 255, 255, {opacity});
                        font-size: 24px;
                        min-width: 15px;
                        max-width: 15px;
                    }}
                """)

        dot_timer = QTimer()
        dot_timer.timeout.connect(update_dots)
        dot_timer.start(50)  # Update every 50ms for smooth animation

        # Create a timer for the 15-second timeout
        timeout_timer = QTimer()
        timeout_timer.setSingleShot(True)

        def handle_timeout():
            dot_timer.stop()
            thinking_bubble.deleteLater()
            ai_reply = "I apologize, but I had to stop processing as it was taking too long. Could you try rephrasing your question or breaking it into smaller parts?"
            self.chat_history.append({"role": "model", "content": ai_reply})
            self.add_chat_bubble(ai_reply, is_user=False, animate=True)
            self.set_send_button_state(False)

        def show_answer():
            try:
                # Call backend Gemini API with timeout parameter
                timeout = 15 if self.deep_thinking_enabled else 5
                resp = requests.post(
                    "http://localhost:5005/chat",
                    json={
                        "messages": self.chat_history,
                        "deep_thinking": self.deep_thinking_enabled,
                        "generate_image": "generate an image" in user_text.lower() or "create an image" in user_text.lower() or "draw" in user_text.lower()
                    },
                    timeout=timeout
                )
                response_data = resp.json()
                ai_reply = response_data.get("response", "Sorry, I couldn't get a response.")
                
                # Check if the response contains an image
                saved_path = None
                if "image" in response_data:
                    image_data = response_data["image"]
                    # Save the image
                    saved_path = self.save_generated_image(image_data)
                    if saved_path:
                        ai_reply = f"I have generated and saved the image to: {saved_path}\n\n{ai_reply}"

                self.chat_history.append({"role": "model", "content": ai_reply})
                dot_timer.stop()
                thinking_bubble.deleteLater()
                self.add_chat_bubble(ai_reply, is_user=False, animate=True)
                timeout_timer.stop()  # Stop the timeout timer as we got a response
                self.set_send_button_state(False)

                # If there was an image, add it to the chat
                if saved_path:
                    self.add_image_to_chat(saved_path, is_user=False)

            except requests.Timeout:
                handle_timeout()
            except Exception as e:
                dot_timer.stop()
                thinking_bubble.deleteLater()
                error_msg = f"Error: {e}"
                self.chat_history.append({"role": "model", "content": error_msg})
                self.add_chat_bubble(error_msg, is_user=False, animate=True)
                timeout_timer.stop()
                self.set_send_button_state(False)

        # Set up the timeout timer if deep thinking is enabled
        if self.deep_thinking_enabled:
            timeout_timer.timeout.connect(handle_timeout)
            timeout_timer.start(15000)  # 15 seconds

        # Start processing in a short delay
        QTimer.singleShot(100, show_answer)

    def open_file_dialog(self):
        if len(self.attached_files) >= 3:
            return  # Maximum 3 files allowed

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)  # Allow multiple file selection
        file_dialog.setNameFilter("All Files (*.*)")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            remaining_slots = 3 - len(self.attached_files)
            
            # Take only as many files as we have slots for
            for file_path in selected_files[:remaining_slots]:
                self.add_file_attachment(file_path)

    def add_file_attachment(self, file_path):
        if len(self.attached_files) >= 3:
            return

        # Create pill
        pill = QFrame()
        pill.setObjectName("filePill")
        pill.setStyleSheet("""
            QFrame#filePill {
                background: rgba(34, 33, 33, 0.5);
                border: none;
                border-radius: 4px;
                min-height: 20px;
                max-height: 20px;
                margin-right: 4px;
                width: 20px;           
            }
        """)
        pill_layout = QHBoxLayout(pill)
        pill_layout.setContentsMargins(7, 0, 7, 0)
        pill_layout.setSpacing(4)

        # Get file info
        file_info = QFileInfo(file_path)
        file_ext = file_info.suffix().lower()

        # File name
        name_label = QLabel(file_info.baseName())
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 11px;
                font-weight: 400;
                background: transparent;
                border: none;
            }
        """)
        pill_layout.addWidget(name_label)

        # File extension label
        if file_ext:
            ext_label = QLabel(f".{file_ext}")
            ext_label.setStyleSheet("""
                QLabel {
                    color: #888;
                    font-size: 11px;
                    font-weight: 400;
                    background: transparent;
                    border: none;
                }
            """)
            pill_layout.addWidget(ext_label)

        # Remove button
        remove_btn = QToolButton()
        remove_btn.setText("×")
        remove_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: none;
                padding: 4px;
                color: #888;
                font-size: 14px;
                font-weight: bold;
            }
            QToolButton:hover {
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                color: #fff;
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_file_attachment(file_path))
        pill_layout.addWidget(remove_btn)

        # Add pill to the container
        self.file_pill_layout.addWidget(pill)
        self.file_pills[file_path] = pill
        self.attached_files.append(file_path)

    def remove_file_attachment(self, file_path):
        if file_path in self.file_pills:
            self.file_pills[file_path].deleteLater()
            self.file_pills.pop(file_path)
            self.attached_files.remove(file_path)

    def clear_chat(self):
        # Clear chat history
        self.chat_history = []
        
        # Clear chat container
        while self.chat_container_layout.count():
            item = self.chat_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Show welcome message again
        self.show_welcome_message()

    def add_image_bubble(self, image_path):
        """Add an image bubble to the chat"""
        # Create container for the image
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create QLabel for the image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        
        # Scale the image if it's too large
        max_size = 400
        if pixmap.width() > max_size or pixmap.height() > max_size:
            pixmap = pixmap.scaled(max_size, max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        image_label.setPixmap(pixmap)
        image_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        
        image_layout.addWidget(image_label)
        
        # Add the image container to chat
        self.chat_container_layout.addWidget(image_container, 0, Qt.AlignLeft)
        
        # Ensure the new message is visible
        QTimer.singleShot(100, lambda: self.chat_scroll.ensureWidgetVisible(image_container))

    def add_chat_bubble(self, text, is_user=False, animate=False):
        def clean_markdown(s):
            # Remove **, __, *, _, ```, etc.
            s = re.sub(r'\*\*\*+', '', s)
            s = re.sub(r'\*\*+', '', s)
            s = re.sub(r'__+', '', s)
            s = re.sub(r'\*+', '', s)
            s = re.sub(r'_+', '', s)
            s = re.sub(r'`+', '', s)
            return s.strip()

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(0)

        bubble = QWidget()
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(20, 16, 20, 16)
        bubble_layout.setSpacing(10)
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        code_match = re.search(r'```[a-zA-Z]*\n([\s\S]+?)```', text)
        code = code_match.group(1).strip() if code_match else None
        explanation = text
        if code:
            explanation = text.replace(code_match.group(0), "").strip()
            explanation = clean_markdown(explanation)

        if code and not is_user:
            code_widget = CodeBlockWidget(code)
            content_layout.addWidget(code_widget)
            if explanation:
                explanation_label = QTextEdit(explanation)
                explanation_label.setWordWrapMode(True)
                explanation_label.setReadOnly(True)
                explanation_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                explanation_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                explanation_label.document().contentsChanged.connect(
                    lambda: explanation_label.setFixedHeight(
                        int(min(explanation_label.document().size().height() + 20, 400))
                    )
                )
                explanation_label.setStyleSheet("""
                    QTextEdit {
                        color: #fff;
                        font-size: 16px;
                        line-height: 1.5;
                        margin-top: 12px;
                        background: transparent;
                        border: none;
                        selection-background-color: #ffffff40;
                        selection-color: #ffffff;
                    }
                """)
                content_layout.addWidget(explanation_label)
        else:
            text_label = QTextEdit(clean_markdown(text))
            text_label.setWordWrapMode(True)
            text_label.setReadOnly(True)
            text_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            text_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            text_label.document().contentsChanged.connect(
                lambda: text_label.setFixedHeight(
                    int(min(text_label.document().size().height() + 20, 400))
                )
            )
            if is_user:
                text_label.setStyleSheet("""
                    QTextEdit {
                        background: #007AFF;
                        color: #fff;
                        border-radius: 16px;
                        padding: 14px 18px;
                        font-size: 18px;
                        line-height: 1.4;
                        max-width: 600px;
                        border: none;
                        selection-background-color: #ffffff40;
                        selection-color: #ffffff;
                    }
                """)
            else:
                text_label.setStyleSheet("""
                    QTextEdit {
                        background: transparent;
                        color: #fff;
                        font-size: 18px;
                        line-height: 1.4;
                        max-width: 600px;
                        border: none;
                        selection-background-color: #ffffff40;
                        selection-color: #ffffff;
                    }
                """)
            content_layout.addWidget(text_label)

        bubble_layout.addWidget(content_container)
        if is_user:
            row_layout.addStretch()
            row_layout.addWidget(bubble, alignment=Qt.AlignRight)
        else:
            row_layout.addWidget(bubble, alignment=Qt.AlignLeft)
            row_layout.addStretch()
        self.chat_container_layout.addWidget(row)
        QTimer.singleShot(100, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))

        if animate:
            if code and not is_user:
                # For code blocks, show copy button immediately but animate the code
                self.animate_text(code_widget.code_label, code_widget.code_label.text())
            else:
                self.animate_text(text_label, text)

    def insert_sample_text(self, text):
        self.line_edit.setText(text)
        self.line_edit.setFocus()
        self.line_edit.cursorForward(False, len(text))

    def hide_sample_buttons(self):
        if self.sample_buttons_widget and self.sample_buttons_shown:
            self.sample_buttons_widget.hide()
            self.sample_buttons_shown = False

    def process_file_for_api(self, file_path):
        file_info = QFileInfo(file_path)
        file_ext = file_info.suffix().lower()
        
        # Handle different file types
        if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            with open(file_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return {
                    'type': 'image',
                    'name': file_info.fileName(),
                    'content': encoded_string
                }
        elif file_ext in ['txt', 'md', 'py', 'js', 'html', 'css', 'json']:
            with open(file_path, 'r', encoding='utf-8') as text_file:
                return {
                    'type': 'text',
                    'name': file_info.fileName(),
                    'content': text_file.read()
                }
        elif file_ext in ['pdf', 'doc', 'docx']:
            # For binary files, send base64 encoded content
            with open(file_path, 'rb') as binary_file:
                encoded_string = base64.b64encode(binary_file.read()).decode('utf-8')
                return {
                    'type': 'document',
                    'name': file_info.fileName(),
                    'content': encoded_string
                }
        else:
            # For unknown types, try to read as text, if fails, send as binary
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return {
                        'type': 'text',
                        'name': file_info.fileName(),
                        'content': file.read()
                    }
            except UnicodeDecodeError:
                with open(file_path, 'rb') as file:
                    encoded_string = base64.b64encode(file.read()).decode('utf-8')
                    return {
                        'type': 'binary',
                        'name': file_info.fileName(),
                        'content': encoded_string
                    }

    def save_generated_image(self, image_data, filename=None):
        """Save a generated image to the Images folder"""
        if not os.path.exists("Images"):
            os.makedirs("Images")
            
        if filename is None:
            # Generate a filename based on timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_image_{timestamp}.png"
            
        filepath = os.path.join("Images", filename)
        
        try:
            # If image_data is base64 encoded
            if isinstance(image_data, str) and "base64" in image_data:
                # Remove the data URL prefix if present
                if "base64," in image_data:
                    image_data = image_data.split("base64,")[1]
                image_bytes = base64.b64decode(image_data)
                with open(filepath, "wb") as f:
                    f.write(image_bytes)
            # If image_data is bytes
            elif isinstance(image_data, bytes):
                with open(filepath, "wb") as f:
                    f.write(image_data)
            # If image_data is a QPixmap or QImage
            elif isinstance(image_data, (QPixmap, QImage)):
                image_data.save(filepath)
                
            return filepath
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    def add_image_to_chat(self, image_path, is_user=False):
        """Add an image to the chat conversation"""
        # Create image container
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(8)
        
        # Load and scale the image
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Create image label
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        image_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        image_layout.addWidget(image_label)
        
        # Add to chat container with proper alignment
        self.chat_container_layout.addWidget(image_container, 0, Qt.AlignLeft if not is_user else Qt.AlignRight)
        
        # Ensure the new message is visible
        QTimer.singleShot(100, self.scroll_to_bottom)
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Create image label
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        image_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        image_layout.addWidget(image_label)
        
        # Add to chat container with proper alignment
        alignment = Qt.AlignRight if is_user else Qt.AlignLeft
        self.chat_container_layout.addWidget(image_container, 0, alignment)
        
        # Ensure the new message is visible
        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """Scroll the chat to the bottom"""
        self.chat_scroll.verticalScrollBar().setValue(self.chat_scroll.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load Poppins font family
    font_regular = QFontDatabase.addApplicationFont("Poppins/Poppins-Regular.ttf")
    font_medium = QFontDatabase.addApplicationFont("Poppins/Poppins-Medium.ttf")
    font_semibold = QFontDatabase.addApplicationFont("Poppins/Poppins-SemiBold.ttf")
    font_bold = QFontDatabase.addApplicationFont("Poppins/Poppins-Bold.ttf")
    
    # Set application-wide font
    if font_regular != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_regular)[0]
        app.setFont(QFont(font_family, 12))  # Increased base font size
    
    # Set global stylesheet for the entire application
    app.setStyleSheet("""
        * {
            font-family: 'Poppins';
        }
        QMainWindow, QWidget {
            background-color: #121212;
            font-family: 'Poppins';
        }
        QLabel {
            font-family: 'Poppins';
            color: #ffffff;
        }
        QPushButton {
            font-family: 'Poppins';
        }
        QLineEdit {
            font-family: 'Poppins';
        }
        QToolButton {
            font-family: 'Poppins';
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
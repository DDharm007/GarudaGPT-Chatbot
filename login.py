# login.py

import sys
import json
import os
import random
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPixmap


class Particle:
    def __init__(self, x, y, dx, dy, size=2, color=QColor(255, 255, 255, 150)):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.color = color

    def move(self, width, height):
        self.x += self.dx
        self.y += self.dy
        # Bounce off the edges
        if self.x <= 0 or self.x >= width:
            self.dx *= -1
        if self.y <= 0 or self.y >= height:
            self.dy *= -1


class ParticleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.particles = []
        self.num_particles = 80
        self.init_particles()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30)

    def init_particles(self):
        width = self.width()
        height = self.height()
        self.particles = []
        for _ in range(self.num_particles):
            x = random.randint(0, width)
            y = random.randint(0, height)
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            size = random.randint(2, 4)
            color = QColor(255, 255, 255, random.randint(100, 200))
            self.particles.append(Particle(x, y, dx, dy, size, color))
        print(f"Initialized {len(self.particles)} particles.")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.init_particles()
        print("ParticleWidget resized.")

    def update_particles(self):
        for particle in self.particles:
            particle.move(self.width(), self.height())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for particle in self.particles:
            painter.setBrush(QBrush(particle.color))
            painter.setPen(Qt.NoPen)
            x = int(particle.x - particle.size)
            y = int(particle.y - particle.size)
            diameter = particle.size * 2
            painter.drawEllipse(x, y, diameter, diameter)
        painter.end()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Garuda.Ai for Programmers - Login")
        self.showFullScreen()
        self.setStyleSheet("background-color: #121212;")

        # Particle Animation
        self.particle_widget = ParticleWidget(self)
        self.particle_widget.resize(self.size())
        self.particle_widget.lower()

        # Main UI
        self.init_ui()

        # Resize handling for particle widget
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.handle_resize)
        self.installEventFilter(self)

        # Ensure a default user exists
        self.ensure_default_user()

    def ensure_default_user(self):
        """
        Checks if 'users.json' exists and contains at least one user.
        If not, creates a default user 'guest' with password 'guest'.
        """
        if not os.path.exists("users.json"):
            with open("users.json", "w") as file:
                default_user_data = {"guest": "guest"}
                json.dump(default_user_data, file, indent=4)
            return

        # If file exists, ensure it's valid JSON with at least one user
        try:
            with open("users.json", "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # Reset to default user if JSON is invalid
            with open("users.json", "w") as file:
                default_user_data = {"guest": "guest"}
                json.dump(default_user_data, file, indent=4)
            return

        # If file is valid JSON but no users, add guest
        if not data:
            data["guest"] = "guest"
            with open("users.json", "w") as file:
                json.dump(data, file, indent=4)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize:
            self.resize_timer.start(100)
        return super().eventFilter(source, event)

    def handle_resize(self):
        self.particle_widget.resize(self.size())

    def init_ui(self):
        central_box_width = 500
        central_box_height = 400
        central_box = QWidget(self)
        central_box.setFixedSize(central_box_width, central_box_height)
        central_box.setStyleSheet("""
            QWidget {
                background-color: rgba(44, 44, 44, 220);
                border-radius: 15px;
            }
        """)

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(40, 30, 40, 30)
        v_layout.setSpacing(15)

        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_path = os.path.join("icons", "logo.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            self.logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.logo_label.setStyleSheet("""
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        else:
            self.logo_label.setText("[Logo]")
            self.logo_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 24px;
                    border: none;
                    background: transparent;
                }
            """)
            print(f"[Warning] logo.png not found at {logo_path}")
        v_layout.addWidget(self.logo_label)

        # Title
        title = QLabel("Join Garuda")
        title.setStyleSheet("color: #ffffff;")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        v_layout.addWidget(title)

        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ffffff;
                border-radius: 8px;
                background-color: #ffffff;
                color: #000000;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        v_layout.addWidget(self.username_input)

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ffffff;
                border-radius: 8px;
                background-color: #ffffff;
                color: #000000;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        v_layout.addWidget(self.password_input)

        v_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dddddd;
                color: black;
            }
            QPushButton:pressed {
                background-color: #cccccc;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(login_btn)

        signup_btn = QPushButton("Signup")
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
                color: white;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        signup_btn.clicked.connect(self.handle_signup)
        btn_layout.addWidget(signup_btn)

        v_layout.addLayout(btn_layout)

        central_box.setLayout(v_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(central_box)
        h_layout.addStretch()
        main_layout.addLayout(h_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def handle_signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        users = self.load_users()
        if username in users:
            QMessageBox.warning(self, "Signup Error", "Username already exists.")
            return

        users[username] = password
        success = self.save_users(users)
        if success:
            self.open_frontend(username)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        users = self.load_users()
        if username in users and users[username] == password:
            self.open_frontend(username)
        else:
            QMessageBox.warning(self, "Login Error", "Invalid username or password.")

    def load_users(self):
        if not os.path.exists("users.json"):
            return {}
        try:
            with open("users.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_users(self, users):
        try:
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save user data: {e}")
            return False

    def open_frontend(self, username):
        try:
            subprocess.Popen([sys.executable, "frontend.py", username])
            self.close()
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "frontend.py not found.")
            self.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open frontend: {e}")
            self.show()


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

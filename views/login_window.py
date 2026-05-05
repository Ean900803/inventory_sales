from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QPushButton, QLabel, QVBoxLayout
)
from PyQt6.QtCore import Qt
from models.employee import Employee
import session


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登入")
        self.setFixedSize(300, 180)
        self._build_ui()

    def _build_ui(self):
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")

        btn_login = QPushButton("登入")
        btn_login.clicked.connect(self._on_login)

        form = QFormLayout()
        form.addRow("帳號", self.username_input)
        form.addRow("密碼", self.password_input)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.error_label)
        layout.addWidget(btn_login)
        self.setLayout(layout)

    def _on_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        emp = Employee.get_by_credentials(username, password)
        if emp:
            session.login(emp)
            self.accept()
        else:
            self.error_label.setText("帳號或密碼錯誤")

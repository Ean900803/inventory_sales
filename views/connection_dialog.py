from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QLineEdit, QSpinBox,
    QDialogButtonBox, QLabel
)


class ConnectionDialog(QDialog):
    """啟動時詢問資料庫連線資訊。預設值來自 config.DB_CONFIG。"""

    def __init__(self, defaults=None):
        super().__init__()
        defaults = defaults or {}
        self.setWindowTitle("資料庫連線")
        self.setFixedWidth(360)
        self._build_ui(defaults)

    def _build_ui(self, d):
        self.host_input = QLineEdit(d.get("host", "localhost"))
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(int(d.get("port", 3306)))
        self.user_input = QLineEdit(d.get("user", "user"))
        self.password_input = QLineEdit(d.get("password", "pw"))
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.database_input = QLineEdit(d.get("database", "inventory_sales"))

        hint = QLabel("首次連線會自動建立資料庫與預設管理員帳號")
        hint.setStyleSheet("color: #5a6577; font-size: 12px;")
        hint.setWordWrap(True)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        form = QFormLayout()
        form.setSpacing(10)
        form.addRow("Host", self.host_input)
        form.addRow("Port", self.port_input)
        form.addRow("帳號", self.user_input)
        form.addRow("密碼", self.password_input)
        form.addRow("資料庫", self.database_input)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addLayout(form)
        layout.addWidget(hint)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_config(self):
        return {
            "host": self.host_input.text().strip(),
            "port": self.port_input.value(),
            "user": self.user_input.text().strip(),
            "password": self.password_input.text(),
            "database": self.database_input.text().strip(),
            "charset": "utf8mb4",
        }

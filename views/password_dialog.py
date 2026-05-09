from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)


class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("重設密碼")
        self._build_ui()

    def _build_ui(self):
        self.new_input = QLineEdit()
        self.new_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow("新密碼", self.new_input)
        layout.addRow("確認新密碼", self.confirm_input)
        layout.addRow(buttons)
        self.setLayout(layout)

    def _on_accept(self):
        new = self.new_input.text()
        confirm = self.confirm_input.text()
        if not new:
            QMessageBox.warning(self, "錯誤", "密碼不可為空")
            return
        if new != confirm:
            QMessageBox.warning(self, "錯誤", "兩次輸入的密碼不一致")
            return
        self.accept()

    def get_password(self):
        return self.new_input.text()

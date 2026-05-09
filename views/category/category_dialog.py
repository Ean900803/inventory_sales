from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)


class CategoryDialog(QDialog):
    def __init__(self, parent=None, category=None):
        super().__init__(parent)
        self.is_edit = category is not None
        self.setWindowTitle("編輯類別" if self.is_edit else "新增類別")
        self._build_ui()
        if category:
            self.name_input.setText(category["name"])

    def _build_ui(self):
        self.name_input = QLineEdit()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow("類別名稱", self.name_input)
        layout.addRow(buttons)
        self.setLayout(layout)

    def _on_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "錯誤", "類別名稱不可為空")
            return
        self.accept()

    def get_data(self):
        return {"name": self.name_input.text().strip()}

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QMessageBox
)


class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer=None):
        super().__init__(parent)
        self.is_edit = customer is not None
        self.setWindowTitle("編輯客戶" if self.is_edit else "新增客戶")
        self._build_ui()
        if customer:
            self._fill(customer)

    def _build_ui(self):
        self.name_input = QLineEdit()
        self.cellphone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.note_input = QTextEdit()
        self.note_input.setFixedHeight(80)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow("姓名", self.name_input)
        layout.addRow("手機", self.cellphone_input)
        layout.addRow("地址", self.address_input)
        layout.addRow("備註", self.note_input)
        layout.addRow(buttons)
        self.setLayout(layout)

    def _fill(self, customer):
        self.name_input.setText(customer["name"])
        self.cellphone_input.setText(customer["cellphone"] or "")
        self.address_input.setText(customer["address"] or "")
        self.note_input.setPlainText(customer["note"] or "")

    def _on_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "錯誤", "客戶姓名不可為空")
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "cellphone": self.cellphone_input.text().strip() or None,
            "address": self.address_input.text().strip() or None,
            "note": self.note_input.toPlainText().strip() or None,
        }

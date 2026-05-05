from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QDialogButtonBox
)


class EmpDialog(QDialog):
    def __init__(self, parent=None, emp=None):
        super().__init__(parent)
        self.setWindowTitle("編輯員工" if emp else "新增員工")
        self._build_ui()
        if emp:
            self._fill(emp)

    def _build_ui(self):
        self.name_input = QLineEdit()
        self.cellphone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.lv_input = QSpinBox()
        self.lv_input.setRange(1, 9)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow("姓名", self.name_input)
        layout.addRow("手機", self.cellphone_input)
        layout.addRow("地址", self.address_input)
        layout.addRow("權限等級", self.lv_input)
        layout.addRow(buttons)
        self.setLayout(layout)

    def _fill(self, emp):
        self.name_input.setText(emp["name"])
        self.cellphone_input.setText(emp["cellphone"])
        self.address_input.setText(emp["address"] or "")
        self.lv_input.setValue(emp["lv"])

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "cellphone": self.cellphone_input.text().strip(),
            "address": self.address_input.text().strip() or None,
            "lv": self.lv_input.value(),
        }

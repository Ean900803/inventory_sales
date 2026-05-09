from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QDialogButtonBox
)
from permissions import is_admin, LV_ADMIN, LV_EMPLOYEE


class EmpDialog(QDialog):
    def __init__(self, parent=None, emp=None):
        super().__init__(parent)
        self.is_edit = emp is not None
        self.setWindowTitle("編輯員工" if self.is_edit else "新增員工")
        self._build_ui()
        if emp:
            self._fill(emp)

    def _build_ui(self):
        self.name_input = QLineEdit()
        self.cellphone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.lv_input = QSpinBox()
        if is_admin():
            self.lv_input.setRange(LV_EMPLOYEE, LV_ADMIN)
        else:
            self.lv_input.setRange(LV_EMPLOYEE, LV_EMPLOYEE)
            self.lv_input.setEnabled(False)

        layout = QFormLayout()
        layout.addRow("姓名", self.name_input)
        if not self.is_edit:
            self.username_input = QLineEdit()
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addRow("帳號", self.username_input)
            layout.addRow("密碼", self.password_input)
        layout.addRow("手機", self.cellphone_input)
        layout.addRow("地址", self.address_input)
        layout.addRow("權限等級", self.lv_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        self.setLayout(layout)

    def _fill(self, emp):
        self.name_input.setText(emp["name"])
        self.cellphone_input.setText(emp["cellphone"])
        self.address_input.setText(emp["address"] or "")
        if emp["lv"] > self.lv_input.maximum():
            self.lv_input.setMaximum(emp["lv"])
        self.lv_input.setValue(emp["lv"])

    def get_data(self):
        data = {
            "name": self.name_input.text().strip(),
            "cellphone": self.cellphone_input.text().strip(),
            "address": self.address_input.text().strip() or None,
            "lv": self.lv_input.value(),
        }
        if not self.is_edit:
            data["username"] = self.username_input.text().strip()
            data["password"] = self.password_input.text().strip()
        return data

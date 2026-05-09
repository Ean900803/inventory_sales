from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit, QComboBox,
    QDoubleSpinBox, QDialogButtonBox, QMessageBox
)


class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None, categories=None):
        super().__init__(parent)
        self.is_edit = product is not None
        self.categories = categories or []
        self.setWindowTitle("編輯商品" if self.is_edit else "新增商品")
        self._build_ui()
        if product:
            self._fill(product)

    def _build_ui(self):
        self.category_input = QComboBox()
        for c in self.categories:
            self.category_input.addItem(c["name"], c["id"])

        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(80)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 999999)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" 元")

        self.cost_input = QDoubleSpinBox()
        self.cost_input.setRange(0, 999999)
        self.cost_input.setDecimals(2)
        self.cost_input.setSuffix(" 元")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow("類別", self.category_input)
        layout.addRow("名稱", self.name_input)
        layout.addRow("描述", self.description_input)
        layout.addRow("售價", self.price_input)
        layout.addRow("成本", self.cost_input)
        layout.addRow(buttons)
        self.setLayout(layout)

    def _fill(self, product):
        idx = self.category_input.findData(product["category_id"])
        if idx >= 0:
            self.category_input.setCurrentIndex(idx)
        self.name_input.setText(product["name"])
        self.description_input.setPlainText(product["description"] or "")
        self.price_input.setValue(float(product["price"]))
        self.cost_input.setValue(float(product["cost"]))

    def _on_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "錯誤", "商品名稱不可為空")
            return
        if self.category_input.currentData() is None:
            QMessageBox.warning(self, "錯誤", "請先建立類別才能新增商品")
            return
        self.accept()

    def get_data(self):
        return {
            "category_id": self.category_input.currentData(),
            "name": self.name_input.text().strip(),
            "description": self.description_input.toPlainText().strip() or None,
            "price": self.price_input.value(),
            "cost": self.cost_input.value(),
        }

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt


class OrderLineRow:
    """單筆明細：把 6 個 widget 塞進 QTableWidget 指定 row 的各 cell"""

    def __init__(self, products, table, row_idx, on_changed, on_remove):
        self._unit_price = 0.0
        self._on_changed = on_changed
        self._table = table

        table.insertRow(row_idx)

        self.product_combo = QComboBox()
        for p in products:
            self.product_combo.addItem(p["name"], p)
        # 不讓 combo 用內容寬度去撐欄寬，靠 column 自己的 Stretch 決定
        self.product_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.product_combo.setMinimumContentsLength(8)
        table.setCellWidget(row_idx, 0, self.product_combo)

        self.qty_input = QSpinBox()
        self.qty_input.setRange(1, 9999)
        table.setCellWidget(row_idx, 1, self.qty_input)

        self.price_item = QTableWidgetItem("0.00")
        self.price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.price_item.setFlags(self.price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row_idx, 2, self.price_item)

        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setSuffix(" %")
        table.setCellWidget(row_idx, 3, self.discount_input)

        self.subtotal_item = QTableWidgetItem("0.00")
        self.subtotal_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.subtotal_item.setFlags(self.subtotal_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row_idx, 4, self.subtotal_item)

        self.btn_remove = QPushButton("移除")
        self.btn_remove.setObjectName("dangerButton")
        self.btn_remove.clicked.connect(lambda: on_remove(self))
        table.setCellWidget(row_idx, 5, self.btn_remove)

        self.product_combo.currentIndexChanged.connect(self._on_product_changed)
        self.qty_input.valueChanged.connect(lambda *_: self._on_changed())
        self.discount_input.valueChanged.connect(lambda *_: self._on_changed())
        self._on_product_changed()

    def current_row(self):
        """回傳這筆明細目前在 table 的 row 索引（其他 row 被刪後會變）"""
        for r in range(self._table.rowCount()):
            if self._table.cellWidget(r, 5) is self.btn_remove:
                return r
        return -1

    def _on_product_changed(self):
        p = self.product_combo.currentData()
        self._unit_price = float(p["price"]) if p else 0.0
        self.price_item.setText(f"{self._unit_price:.2f}")
        self._on_changed()

    def subtotal(self):
        return (
            self.qty_input.value()
            * self._unit_price
            * (1 - self.discount_input.value() / 100)
        )

    def update_subtotal(self):
        self.subtotal_item.setText(f"{self.subtotal():.2f}")

    def get_data(self):
        p = self.product_combo.currentData()
        if p is None:
            return None
        return {
            "product_id": p["id"],
            "quantity": self.qty_input.value(),
            "price": self._unit_price,
            "cost": float(p["cost"]),
            "discount": self.discount_input.value(),
        }


class OrderDialog(QDialog):
    """新增訂單：選客戶 + 多筆商品明細（單價鎖死，僅折扣可調）"""

    HEADERS = ["商品", "數量", "單價", "折扣", "小計", "移除"]

    def __init__(self, parent=None, customers=None, products=None):
        super().__init__(parent)
        self.products = products or []
        self.rows = []
        self.setWindowTitle("新增訂單")
        self.resize(820, 520)
        self._build_ui(customers or [])
        self._add_row()

    def _build_ui(self, customers):
        self.customer_combo = QComboBox()
        for c in customers:
            self.customer_combo.addItem(c["name"], c["id"])

        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        header = self.table.horizontalHeader()
        # 預設 stretchLastSection=True 會強迫最後一欄(移除)吃掉所有剩餘空間，蓋掉我設的 Fixed
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)            # 商品
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)   # 數量
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)   # 單價
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)   # 折扣
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)   # 小計
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)              # 移除
        self.table.setColumnWidth(5, 88)

        self.btn_add_row = QPushButton("＋ 新增明細")
        self.btn_add_row.clicked.connect(self._add_row)

        self.total_label = QLabel("總計：0.00 元")
        self.total_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        form = QFormLayout()
        form.addRow("客戶", self.customer_combo)

        bottom_bar = QHBoxLayout()
        bottom_bar.addWidget(self.btn_add_row)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.total_label)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.table, 1)
        layout.addLayout(bottom_bar)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def _add_row(self):
        if not self.products:
            QMessageBox.warning(self, "錯誤", "尚未建立商品")
            return
        row = OrderLineRow(
            self.products, self.table, self.table.rowCount(),
            on_changed=self._refresh_totals,
            on_remove=self._remove_row,
        )
        self.rows.append(row)
        self.table.resizeRowToContents(self.table.rowCount() - 1)
        self._refresh_totals()

    def _remove_row(self, row):
        if len(self.rows) <= 1:
            QMessageBox.information(self, "提示", "至少需要一筆明細")
            return
        r = row.current_row()
        if r >= 0:
            self.table.removeRow(r)
        self.rows.remove(row)
        self._refresh_totals()

    def _refresh_totals(self):
        total = 0
        for row in self.rows:
            row.update_subtotal()
            total += row.subtotal()
        self.total_label.setText(f"總計：{total:.2f} 元")

    def _on_accept(self):
        if self.customer_combo.currentData() is None:
            QMessageBox.warning(self, "錯誤", "請先建立客戶才能新增訂單")
            return
        records = [r.get_data() for r in self.rows if r.get_data()]
        if not records:
            QMessageBox.warning(self, "錯誤", "至少需要一筆明細")
            return
        self.accept()

    def get_data(self):
        return {
            "customer_id": self.customer_combo.currentData(),
            "records": [r.get_data() for r in self.rows if r.get_data()],
        }


class OrderStatusDialog(QDialog):
    """編輯訂單狀態（不改明細）"""

    def __init__(self, parent=None, order=None, records=None):
        super().__init__(parent)
        from models.order import ORDER_STATUSES, STATUS_LABELS
        self.order = order
        self.records = records or []
        self.setWindowTitle(f"編輯訂單 #{order['id']}")
        self.resize(500, 400)

        self.status_combo = QComboBox()
        for s in ORDER_STATUSES:
            self.status_combo.addItem(STATUS_LABELS[s], s)
        idx = self.status_combo.findData(order["status"])
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)

        lines = ["商品 / 數量 / 單價 / 折扣"]
        total = 0
        for r in self.records:
            subtotal = float(r["price"]) * r["quantity"] * (1 - float(r["discount"]) / 100)
            total += subtotal
            lines.append(
                f"・{r['product_name']}　×{r['quantity']}　"
                f"@{float(r['price']):.2f}　-{float(r['discount']):.0f}%　"
                f"= {subtotal:.2f}"
            )
        lines.append(f"\n總計：{total:.2f} 元")
        records_label = QLabel("\n".join(lines))
        records_label.setWordWrap(True)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        form = QFormLayout()
        form.addRow("客戶", QLabel(order["customer_name"]))
        form.addRow("訂購日", QLabel(str(order["ordered_date"])))
        form.addRow("狀態", self.status_combo)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(QLabel("明細："))
        layout.addWidget(records_label)
        layout.addStretch()
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_status(self):
        return self.status_combo.currentData()

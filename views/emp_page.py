from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel
)


class EmpPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "姓名", "手機", "地址", "權限等級"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.btn_add = QPushButton("新增")
        self.btn_edit = QPushButton("編輯")
        self.btn_resign = QPushButton("離職")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_resign)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("員工管理"))
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self, employees):
        self.table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(str(emp["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(emp["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(emp["cellphone"]))
            self.table.setItem(row, 3, QTableWidgetItem(emp["address"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(str(emp["lv"])))

    def get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 0).text())

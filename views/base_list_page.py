from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
)


class BaseListPage(QWidget):
    """共用的清單頁面：標題 + 右上按鈕列 + 表格。子類只描述欄位與按鈕。"""

    def __init__(self, title, columns):
        super().__init__()
        self._title = title
        self._columns = columns
        self._build_ui()

    def _build_ui(self):
        self.title_label = QLabel(self._title)
        self.title_label.setObjectName("pageTitle")

        self.table = QTableWidget()
        self.table.setColumnCount(len(self._columns))
        self.table.setHorizontalHeaderLabels(self._columns)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.button_bar = QHBoxLayout()
        self.button_bar.addStretch()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addLayout(self.button_bar)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_button(self, text, *, danger=False):
        btn = QPushButton(text)
        if danger:
            btn.setObjectName("dangerButton")
        self.button_bar.addWidget(btn)
        return btn

    def load_rows(self, rows, fields):
        """rows: list[dict]；fields: 對應 columns 順序的欄位名。"""
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, field in enumerate(fields):
                value = row.get(field)
                text = "" if value is None else str(value)
                self.table.setItem(r, c, QTableWidgetItem(text))

    def get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if item is None:
            return None
        return int(item.text())

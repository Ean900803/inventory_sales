from PyQt6.QtWidgets import QTableWidgetItem
from views.base_list_page import BaseListPage
from models.order import STATUS_LABELS


class OrderPage(BaseListPage):
    def __init__(self):
        super().__init__("訂單管理", ["ID", "客戶", "訂購日", "狀態", "總額"])
        self.btn_add = self.add_button("新增訂單")
        self.btn_edit = self.add_button("編輯狀態")
        self.btn_cancel = self.add_button("取消訂單", danger=True)

    def load_data(self, orders):
        self.table.setRowCount(len(orders))
        for r, o in enumerate(orders):
            self.table.setItem(r, 0, QTableWidgetItem(str(o["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(o["customer_name"]))
            self.table.setItem(r, 2, QTableWidgetItem(str(o["ordered_date"])))
            self.table.setItem(r, 3, QTableWidgetItem(STATUS_LABELS.get(o["status"], o["status"])))
            self.table.setItem(r, 4, QTableWidgetItem(f"{float(o['total']):.2f}"))

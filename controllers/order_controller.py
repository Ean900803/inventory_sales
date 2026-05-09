from PyQt6.QtWidgets import QMessageBox
from models.order import Order
from models.customer import Customer
from models.product import Product
from views.order.order_dialog import OrderDialog, OrderStatusDialog
from permissions import has_lv, LV_EMPLOYEE, LV_MANAGER


class OrderController:
    def __init__(self, page):
        self.page = page
        self.load()
        self.page.btn_add.clicked.connect(self._on_add)
        self.page.btn_edit.clicked.connect(self._on_edit)
        self.page.btn_cancel.clicked.connect(self._on_cancel)
        self._apply_permissions()

    def load(self):
        self.page.load_data(Order.get_all())

    def _apply_permissions(self):
        """1:可以建立 >=3:可以編輯跟取消"""
        self.page.btn_add.setVisible(has_lv(LV_EMPLOYEE))
        self.page.btn_edit.setVisible(has_lv(LV_MANAGER))
        self.page.btn_cancel.setVisible(has_lv(LV_MANAGER))

    def _on_add(self):
        """綁定新增"""
        if not has_lv(LV_EMPLOYEE):
            return
        customers = Customer.get_all()
        if not customers:
            QMessageBox.warning(self.page, "錯誤", "尚未建立客戶")
            return
        products = Product.get_active()
        if not products:
            QMessageBox.warning(self.page, "錯誤", "尚未建立商品")
            return
        dialog = OrderDialog(self.page, customers=customers, products=products)
        if dialog.exec() != OrderDialog.DialogCode.Accepted:
            return
        Order.create(**dialog.get_data())
        self.load()

    def _on_edit(self):
        """綁定編輯"""
        if not has_lv(LV_MANAGER):
            return
        order_id = self.page.get_selected_id()
        if order_id is None:
            QMessageBox.warning(self.page, "請選擇訂單", "請先選取一筆訂單")
            return
        order, records = Order.get_with_records(order_id)
        if order is None:
            return
        dialog = OrderStatusDialog(self.page, order=order, records=records)
        if dialog.exec() != OrderStatusDialog.DialogCode.Accepted:
            return
        Order.update_status(order_id, dialog.get_status())
        self.load()

    def _on_cancel(self):
        """綁定取消"""
        if not has_lv(LV_MANAGER):
            return
        order_id = self.page.get_selected_id()
        if order_id is None:
            QMessageBox.warning(self.page, "請選擇訂單", "請先選取一筆訂單")
            return
        confirm = QMessageBox.question(
            self.page, "確認取消",
            "確定要取消此訂單？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            Order.cancel(order_id)
            self.load()

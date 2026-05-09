from PyQt6.QtWidgets import QMessageBox
from models.customer import Customer
from views.customer.customer_dialog import CustomerDialog
from permissions import has_lv, LV_SALES


class CustomerController:
    def __init__(self, page):
        self.page = page
        self.load()
        self.page.btn_add.clicked.connect(self._on_add)
        self.page.btn_edit.clicked.connect(self._on_edit)
        self._apply_permissions()

    def load(self):
        self.page.load_data(Customer.get_all())

    def _apply_permissions(self):
        can = has_lv(LV_SALES)
        self.page.btn_add.setVisible(can)
        self.page.btn_edit.setVisible(can)

    def _on_add(self):
        """綁定新增"""
        if not has_lv(LV_SALES):
            return
        dialog = CustomerDialog(self.page)
        if dialog.exec() != CustomerDialog.DialogCode.Accepted:
            return
        Customer.create(**dialog.get_data())
        self.load()

    def _on_edit(self):
        """綁定編輯"""
        if not has_lv(LV_SALES):
            return
        customer_id = self.page.get_selected_id()
        if customer_id is None:
            QMessageBox.warning(self.page, "請選擇客戶", "請先選取一筆客戶資料")
            return
        customer = Customer.get_by_id(customer_id)
        if customer is None:
            return
        dialog = CustomerDialog(self.page, customer=customer)
        if dialog.exec() != CustomerDialog.DialogCode.Accepted:
            return
        Customer.update(customer_id, **dialog.get_data())
        self.load()

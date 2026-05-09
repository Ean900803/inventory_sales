from PyQt6.QtWidgets import QMessageBox
from models.product import Product
from models.category import Category
from views.product.product_dialog import ProductDialog
from permissions import has_lv, is_admin, LV_PRODUCT


class ProductController:
    def __init__(self, page):
        self.page = page
        self.load()
        self.page.btn_add.clicked.connect(self._on_add)
        self.page.btn_edit.clicked.connect(self._on_edit)
        self.page.btn_disable.clicked.connect(self._on_disable)
        self.page.btn_restore.clicked.connect(self._on_restore)
        self._apply_permissions()

    def load(self):
        self.page.load_data(Product.get_all())

    def _apply_permissions(self):
        """權限2才可以編輯刪除"""
        can = has_lv(LV_PRODUCT)
        self.page.btn_add.setVisible(can)
        self.page.btn_edit.setVisible(can)
        self.page.btn_disable.setVisible(can)
        self.page.btn_restore.setVisible(is_admin())

    def _on_add(self):
        """綁定新增按鈕"""
        if not has_lv(LV_PRODUCT):
            return
        dialog = ProductDialog(self.page, categories=Category.get_active())
        if dialog.exec() != ProductDialog.DialogCode.Accepted:
            return
        Product.create(**dialog.get_data())
        self.load()

    def _on_edit(self):
        """綁定編輯按鈕"""
        if not has_lv(LV_PRODUCT):
            return
        product_id = self.page.get_selected_id()
        if product_id is None:
            QMessageBox.warning(self.page, "請選擇商品", "請先選取一筆商品資料")
            return
        product = Product.get_by_id(product_id)
        if product is None:
            return
        dialog = ProductDialog(self.page, product=product, categories=Category.get_active())
        if dialog.exec() != ProductDialog.DialogCode.Accepted:
            return
        Product.update(product_id, **dialog.get_data())
        self.load()

    def _on_disable(self):
        """綁定刪除"""
        if not has_lv(LV_PRODUCT):
            return
        product_id = self.page.get_selected_id()
        if product_id is None:
            QMessageBox.warning(self.page, "請選擇商品", "請先選取一筆商品資料")
            return
        confirm = QMessageBox.question(
            self.page, "確認停用",
            "確定要停用此商品？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            Product.disable(product_id)
            self.load()

    def _on_restore(self):
        """綁定復原"""
        if not is_admin():
            return
        product_id = self.page.get_selected_id()
        if product_id is None:
            QMessageBox.warning(self.page, "請選擇商品", "請先選取一筆商品資料")
            return
        confirm = QMessageBox.question(
            self.page, "確認復原",
            "確定要復原此商品？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            Product.restore(product_id)
            self.load()

from PyQt6.QtWidgets import QMessageBox
from models.category import Category
from views.category.category_dialog import CategoryDialog
from permissions import has_lv, is_admin, LV_PRODUCT


class CategoryController:
    def __init__(self, page):
        self.page = page
        self.load()
        self.page.btn_add.clicked.connect(self._on_add)
        self.page.btn_edit.clicked.connect(self._on_edit)
        self.page.btn_disable.clicked.connect(self._on_disable)
        self.page.btn_restore.clicked.connect(self._on_restore)
        self._apply_permissions()

    def load(self):
        categories = Category.get_all()
        self.page.load_data(categories)

    def _apply_permissions(self):
        can = has_lv(LV_PRODUCT)
        self.page.btn_add.setVisible(can)
        self.page.btn_edit.setVisible(can)
        self.page.btn_disable.setVisible(can)
        self.page.btn_restore.setVisible(is_admin())

    def _on_add(self):
        if not has_lv(LV_PRODUCT):
            return
        dialog = CategoryDialog(self.page)
        if dialog.exec() != CategoryDialog.DialogCode.Accepted:
            return
        Category.create(**dialog.get_data())
        self.load()

    def _on_edit(self):
        if not has_lv(LV_PRODUCT):
            return
        category_id = self.page.get_selected_id()
        if category_id is None:
            QMessageBox.warning(self.page, "請選擇類別", "請先選取一筆類別資料")
            return
        category = next(
            (c for c in Category.get_all() if c["id"] == category_id), None
        )
        if category is None:
            return
        dialog = CategoryDialog(self.page, category=category)
        if dialog.exec() != CategoryDialog.DialogCode.Accepted:
            return
        Category.update(category_id, **dialog.get_data())
        self.load()

    def _on_disable(self):
        if not has_lv(LV_PRODUCT):
            return
        category_id = self.page.get_selected_id()
        if category_id is None:
            QMessageBox.warning(self.page, "請選擇類別", "請先選取一筆類別資料")
            return
        confirm = QMessageBox.question(
            self.page, "確認停用",
            "確定要停用此類別？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            Category.disable(category_id)
            self.load()

    def _on_restore(self):
        if not is_admin():
            return
        category_id = self.page.get_selected_id()
        if category_id is None:
            QMessageBox.warning(self.page, "請選擇類別", "請先選取一筆類別資料")
            return
        confirm = QMessageBox.question(
            self.page, "確認復原",
            "確定要復原此類別？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            Category.restore(category_id)
            self.load()

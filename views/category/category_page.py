from views.base_list_page import BaseListPage


class CategoryPage(BaseListPage):
    def __init__(self):
        super().__init__("類別管理", ["ID", "類別名稱", "停用日"])
        self.btn_add = self.add_button("新增")
        self.btn_edit = self.add_button("編輯")
        self.btn_disable = self.add_button("停用", danger=True)
        self.btn_restore = self.add_button("復原")

    def load_data(self, categories):
        self.load_rows(categories, ["id", "name", "deleted_at"])

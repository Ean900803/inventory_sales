from views.base_list_page import BaseListPage


class ProductPage(BaseListPage):
    def __init__(self):
        super().__init__("商品管理", ["ID", "名稱", "類別", "售價", "成本", "停用日"])
        self.btn_add = self.add_button("新增")
        self.btn_edit = self.add_button("編輯")
        self.btn_disable = self.add_button("停用", danger=True)
        self.btn_restore = self.add_button("復原")

    def load_data(self, products):
        self.load_rows(
            products,
            ["id", "name", "category_name", "price", "cost", "deleted_at"],
        )

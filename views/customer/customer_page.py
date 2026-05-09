from views.base_list_page import BaseListPage


class CustomerPage(BaseListPage):
    def __init__(self):
        super().__init__("客戶管理", ["ID", "姓名", "手機", "地址", "備註"])
        self.btn_add = self.add_button("新增")
        self.btn_edit = self.add_button("編輯")

    def load_data(self, customers):
        self.load_rows(customers, ["id", "name", "cellphone", "address", "note"])

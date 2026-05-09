from views.base_list_page import BaseListPage


class EmpPage(BaseListPage):
    def __init__(self):
        super().__init__("員工管理", ["ID", "姓名", "手機", "地址", "權限等級", "離職日"])
        self.btn_add = self.add_button("新增")
        self.btn_edit = self.add_button("編輯")
        self.btn_reset_pw = self.add_button("重設密碼")
        self.btn_resign = self.add_button("離職", danger=True)
        self.btn_restore = self.add_button("復職")

    def load_data(self, employees):
        self.load_rows(
            employees,
            ["id", "name", "cellphone", "address", "lv", "resigned_date"],
        )

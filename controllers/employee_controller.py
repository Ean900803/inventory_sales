from PyQt6.QtWidgets import QMessageBox
from models.employee import Employee
from views.emp_dialog import EmpDialog


class EmployeeController:
    def __init__(self, page):
        self.page = page
        self.load()
        self.page.btn_add.clicked.connect(self._on_add)
        self.page.btn_edit.clicked.connect(self._on_edit)
        self.page.btn_resign.clicked.connect(self._on_resign)

    def load(self):
        employees = Employee.get_all()
        self.page.load_data(employees)

    def _on_add(self):
        dialog = EmpDialog(self.page)
        if dialog.exec() != EmpDialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        Employee.create(**data)
        self.load()

    def _on_edit(self):
        emp_id = self.page.get_selected_id()
        if emp_id is None:
            QMessageBox.warning(self.page, "請選擇員工", "請先選取一筆員工資料")
            return
        emp = Employee.get_by_id(emp_id)
        dialog = EmpDialog(self.page, emp=emp)
        if dialog.exec() != EmpDialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        Employee.update(emp_id, **data)
        self.load()

    def _on_resign(self):
        emp_id = self.page.get_selected_id()
        if emp_id is None:
            QMessageBox.warning(self.page, "請選擇員工", "請先選取一筆員工資料")
            return
        confirm = QMessageBox.question(
            self.page, "確認離職",
            "確定要將此員工設為離職？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            Employee.resign(emp_id)
            self.load()

from PyQt6.QtWidgets import QMessageBox
from models.employee import Employee
from views.emp.emp_dialog import EmpDialog
from views.password_dialog import PasswordDialog
import session
from permissions import is_admin


class EmployeeController:
    def __init__(self, page):
        self.page = page
        self.load()
        self.page.btn_add.clicked.connect(self._on_add)
        self.page.btn_edit.clicked.connect(self._on_edit)
        self.page.btn_reset_pw.clicked.connect(self._on_reset_pw)
        self.page.btn_resign.clicked.connect(self._on_resign)
        self.page.btn_restore.clicked.connect(self._on_restore)
        self._apply_permissions()

    def load(self):
        employees = Employee.get_all(include_resigned=is_admin())
        self.page.load_data(employees)

    def _can_edit_emp(self, emp_id):
        user = session.get()
        return user is not None and (is_admin() or user["id"] == emp_id)

    def _apply_permissions(self):
        admin = is_admin()
        self.page.btn_add.setVisible(admin)
        self.page.btn_resign.setVisible(admin)
        self.page.btn_restore.setVisible(admin)

    def _on_add(self):
        """綁定新增"""
        if not is_admin():
            return
        dialog = EmpDialog(self.page)
        if dialog.exec() != EmpDialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        Employee.create(**data)
        self.load()

    def _on_edit(self):
        """綁定編輯"""
        emp_id = self.page.get_selected_id()
        if emp_id is None:
            QMessageBox.warning(self.page, "請選擇員工", "請先選取一筆員工資料")
            return
        if not self._can_edit_emp(emp_id):
            QMessageBox.warning(self.page, "權限不足", "只有管理員或本人可以編輯此資料")
            return
        emp = Employee.get_by_id(emp_id)
        dialog = EmpDialog(self.page, emp=emp)
        if dialog.exec() != EmpDialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        Employee.update(emp_id, **data)
        self.load()

    def _on_reset_pw(self):
        """綁定reset pw btn"""
        emp_id = self.page.get_selected_id()
        if emp_id is None:
            QMessageBox.warning(self.page, "請選擇員工", "請先選取一筆員工資料")
            return
        if not self._can_edit_emp(emp_id):
            QMessageBox.warning(self.page, "權限不足", "只有管理員或本人可以重設此密碼")
            return
        dialog = PasswordDialog(self.page)
        if dialog.exec() != PasswordDialog.DialogCode.Accepted:
            return
        Employee.reset_password(emp_id, dialog.get_password())
        QMessageBox.information(self.page, "成功", "密碼已重設")

    def _on_resign(self):
        """綁定離職"""
        if not is_admin():
            return
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

    def _on_restore(self):
        """綁定回覆"""
        if not is_admin():
            return
        emp_id = self.page.get_selected_id()
        if emp_id is None:
            QMessageBox.warning(self.page, "請選擇員工", "請先選取一筆員工資料")
            return
        confirm = QMessageBox.question(
            self.page, "確認復職",
            "確定要將此員工復職？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            Employee.restore(emp_id)
            self.load()

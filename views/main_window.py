from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QStackedWidget, QLabel, QPushButton
)
from PyQt6.QtCore import QSize, pyqtSignal
from views.emp_page import EmpPage
from controllers.employee_controller import EmployeeController
import session


class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("訂單管理系統")
        self.resize(691, 600)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        emp = session.get()
        self.user_label = QLabel(f"登入者：{emp['name']}" if emp else "")
        self.btn_logout = QPushButton("登出")

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.user_label)
        top_bar.addWidget(self.btn_logout)

        self.sideBar = QListWidget()
        self.sideBar.setMaximumSize(QSize(150, 16777215))

        self.emp = EmpPage()
        self.product = QWidget()
        self.category = QWidget()
        self.customer = QWidget()
        self.order = QWidget()

        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.emp)
        self.content_stack.addWidget(self.product)
        self.content_stack.addWidget(self.category)
        self.content_stack.addWidget(self.customer)
        self.content_stack.addWidget(self.order)

        self.page_map = {
            "員工管理": self.emp,
            "商品管理": self.product,
            "類別管理": self.category,
            "客戶管理": self.customer,
            "訂單管理": self.order,
        }
        self.sideBar.addItems(list(self.page_map.keys()))

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.sideBar)
        content_layout.addWidget(self.content_stack)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_bar)
        main_layout.addLayout(content_layout)

        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def _connect_signals(self):
        self.sideBar.currentTextChanged.connect(self._switch_page)
        self.btn_logout.clicked.connect(self._on_logout)
        self.emp_ctrl = EmployeeController(self.emp)

    def _switch_page(self, text):
        page = self.page_map.get(text)
        if page:
            self.content_stack.setCurrentWidget(page)

    def _on_logout(self):
        session.logout()
        self.logout_requested.emit()
        self.close()

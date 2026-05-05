import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from database import test_connection
from views.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("訂單管理系統")
        self.page_map = {
            "員工管理": self.ui.emp,
            "商品管理": self.ui.product,
            "類別管理": self.ui.category,
            "客戶管理": self.ui.customer,
            "訂單管理": self.ui.order
        }

        self.ui.sideBar.currentTextChanged.connect(self.switch_page)
    def switch_page(self, text):
        page = self.page_map.get(text)
        if page:
            self.ui.content_stack.setCurrentWidget(page)

def main():
    app = QApplication(sys.argv)
    if not test_connection():
        QMessageBox.critical(None, "連線失敗", "資料庫連線失敗，請檢查.env設定")
        sys.exit(1)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
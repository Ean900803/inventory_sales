import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from database import test_connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("訂單管理系統")
        self.resize(1200, 800)
        self.setCentralWidget(QLabel("Hello OMS", self))

def main():
    if not test_connection():
        print("資料庫連線失敗，請檢查 .env 設定")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
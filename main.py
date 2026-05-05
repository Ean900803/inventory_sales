import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import test_connection
from views.login_window import LoginWindow
from views.main_window import MainWindow
import session


def main():
    app = QApplication(sys.argv)
    if not test_connection():
        QMessageBox.critical(None, "連線失敗", "資料庫連線失敗，請檢查.env設定")
        sys.exit(1)

    while True:
        login = LoginWindow()
        if login.exec() != LoginWindow.DialogCode.Accepted:
            break

        window = MainWindow()
        window.show()
        app.exec()

        # 登出時 session 已被清空，繼續迴圈回到登入頁
        # 直接按 X 關閉時 session 仍有值，結束程式
        if session.get() is not None:
            break

    sys.exit(0)


if __name__ == "__main__":
    main()

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from config import DB_CONFIG
from database import setup_database
from views.connection_dialog import ConnectionDialog
from views.login_window import LoginWindow
from views.main_window import MainWindow
from views.style import APP_STYLE
import session


def _ensure_database():
    """跳出 ConnectionDialog 直到使用者輸入可用的連線（或選擇取消）。"""
    while True:
        dialog = ConnectionDialog(defaults=DB_CONFIG)
        if dialog.exec() != ConnectionDialog.DialogCode.Accepted:
            return False
        config = dialog.get_config()
        try:
            initialized = setup_database(config)
        except Exception as e:
            QMessageBox.critical(None, "連線失敗", f"無法連線或初始化：\n{e}")
            continue

        DB_CONFIG.update(config)
        if initialized:
            QMessageBox.information(
                None, "初始化完成",
                "已建立資料庫並寫入預設管理員：\n\n帳號：admin\n密碼：admin\n\n請登入後立即修改密碼。",
            )
        return True


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    if not _ensure_database():
        sys.exit(0)

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

APP_STYLE = """
* {
    font-family: "Segoe UI", "Microsoft JhengHei", "PingFang TC", sans-serif;
    font-size: 13px;
    color: #2c3e50;
}

QMainWindow, QDialog, QWidget#centralWidget {
    background-color: #f5f6fa;
}

QLabel#pageTitle {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    padding: 4px 0 8px 0;
    border-bottom: 2px solid #4a90e2;
}

QLabel#userLabel {
    color: #5a6577;
    padding-right: 6px;
}

QPushButton {
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 16px;
    min-width: 64px;
}
QPushButton:hover { background-color: #357abd; }
QPushButton:pressed { background-color: #2c5d8f; }
QPushButton:disabled { background-color: #b8c4d1; color: #f0f0f0; }

QPushButton#dangerButton { background-color: #dc3545; }
QPushButton#dangerButton:hover { background-color: #b02a37; }
QPushButton#dangerButton:pressed { background-color: #8b1f2b; }

QPushButton#logoutButton {
    background-color: transparent;
    color: #5a6577;
    border: 1px solid #c8d0db;
}
QPushButton#logoutButton:hover {
    background-color: #ecf0f5;
    color: #2c3e50;
}

QListWidget#sideBar {
    background-color: #2c3e50;
    border: none;
    padding: 8px 6px;
    outline: none;
}
QListWidget#sideBar::item {
    color: #cfd6df;
    padding: 12px 14px;
    border-radius: 4px;
    margin: 2px 0;
}
QListWidget#sideBar::item:hover {
    background-color: #3a5168;
    color: white;
}
QListWidget#sideBar::item:selected {
    background-color: #4a90e2;
    color: white;
}

QTableWidget {
    background-color: white;
    alternate-background-color: #f8fafc;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    gridline-color: #ecf0f5;
    selection-background-color: #4a90e2;
    selection-color: white;
}
QTableWidget::item { padding: 6px; }

QHeaderView::section {
    background-color: #f0f3f7;
    color: #2c3e50;
    padding: 8px 6px;
    border: none;
    border-right: 1px solid #dcdfe6;
    border-bottom: 1px solid #dcdfe6;
    font-weight: 600;
}
QHeaderView::section:last { border-right: none; }

QLineEdit, QTextEdit, QPlainTextEdit, QAbstractSpinBox, QComboBox {
    background-color: white;
    color: #2c3e50;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    padding: 6px 8px;
    selection-background-color: #4a90e2;
    selection-color: white;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QAbstractSpinBox:focus, QComboBox:focus { border-color: #4a90e2; }

QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled,
QAbstractSpinBox:disabled, QComboBox:disabled {
    background-color: #f0f3f7;
    color: #8a95a7;
}

QComboBox QAbstractItemView {
    background-color: white;
    color: #2c3e50;
    border: 1px solid #dcdfe6;
    selection-background-color: #4a90e2;
    selection-color: white;
    outline: none;
}
QLabel#errorLabel { color: #dc3545; }
"""

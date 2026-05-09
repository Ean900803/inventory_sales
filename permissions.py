import session

# 採線性權限：高 lv 自動包含低 lv 能力
LV_EMPLOYEE = 1            # 建立訂單
LV_SALES    = 2            # + 建立客戶 / 管理產品 / 管理類別
LV_PRODUCT  = LV_SALES     # 別名：與 LV_SALES 同階
LV_MANAGER  = 3            # + 編輯/取消訂單
LV_ADMIN    = 9            # + 管理員工


def current_lv():
    user = session.get()
    return user["lv"] if user else 0


def has_lv(min_lv):
    return current_lv() >= min_lv


def is_admin():
    return has_lv(LV_ADMIN)

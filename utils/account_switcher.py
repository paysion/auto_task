import core.adb as adb
import utils.account_switcher as account_switcher
from config.accounts import ACCOUNTS, CURRENT_INDEX

def logout():
    """退出当前账号"""
    print("正在退出账号…")

    # 打开 “我的”
    adb.tap(800, 1525)

    # 打开设置
    print("点击顶部设置按钮, 330 220")
    adb.tap(330, 220)

    # 点击 “退出登录”
    print("点击退出登录按钮, 450 1500")
    adb.tap(450, 1500)

    # 确认
    print("点击确认按钮, 605 900")
    adb.tap(605, 900)

    print("退出成功！")


def login(username, password):
    """登录账号"""
    print(f"正在登录账号：{username}")
    # 打开 “我的”
    adb.tap(800, 1525)
    # 点击登录
    print("点击登录按钮, 330 220")
    adb.tap(330, 220)
    # 切换账号密码登录
    print("点击切换账号密码登录按钮, 100 490")
    adb.tap(100, 490)

    # 输入账号
    adb.tap(100, 360)
    adb.input_text(username)

    # 输入密码
    adb.tap(100, 520)
    adb.input_text(password)

    # 点击登录
    adb.tap(450, 650)
    # 点击同意并登录
    print("点击同意并登录按钮, 605 900")
    adb.tap(605, 900)

    print(f"账号 {username} 登录成功！")

def switch_to_next_account():
    """从账号列表自动切换到下一个账号"""

    global CURRENT_INDEX

    next_index = (CURRENT_INDEX + 1) % len(ACCOUNTS)
    account = ACCOUNTS[next_index]
    
    print(f"切换账号：{CURRENT_INDEX} → {next_index}")

    # 退出
    logout()

    # 登录
    login(account["username"], account["password"])

    # 更新索引
    CURRENT_INDEX = next_index

    print(f"当前账号已切换为：{account['username']}")


import core.adb as adb
import core.template_match as template_match
import core.ocr as ocr
from config.accounts import ACCOUNTS, CURRENT_INDEX
import config.settings as settings
# from tasks.task import safe_run


def logout():
    """退出当前账号"""
    print("==[info]==📢正在退出账号…")
    mine_btn_paths = [settings.MINE_BTN_PATH, settings.MINE_BTN_02_PATH, settings.MINE_BTN_03_PATH, settings.MINE_BTN_04_PATH]
    x, y, score, path = template_match.find_best_template(adb.screencap(), mine_btn_paths)
    if x is not None:
        print(f"==[info]==📢匹配度最高的[我的]按钮：{path}，score={score:.2f}")
    else:
        print("==[error]==❌ 未找到我的按钮，请检查是否在首页")
        return False
    
    
    # 打开 “我的”
    mine_success = adb.wait_and_tap("打开我的", 800, 1525, x, y)
    #adb.tap(800, 1525)
    if not mine_success:
        print("==[ERROR]==❌ 打开[我的]失败")
        return False
    # 打开设置
    print("==[info]==📢点击顶部设置按钮, 330 220")
    adb.tap(330, 220)

    # 点击 “退出登录”
    print("==[info]==📢点击退出登录按钮, 450 1500")
    #adb.tap(450, 1500)
    logout_btn_paths = [settings.LOGOUT_BTN_PATH]
    x1, y1, score1, path1 = template_match.find_best_template(adb.screencap(), logout_btn_paths)
    if x1 is not None:
        print(f"==[info]==📢匹配度最高的[退出登录]按钮：{path1}，score={score1:.2f}")
    else:
        print("==[error]==❌ 未找到[退出登录]按钮，请检查是否在设置页面")
    logout_success = adb.wait_and_tap("退出登录", 450, 1500,x1, y1)
    if not logout_success:
        print("==[ERROR]==❌ 退出登录失败")
        return False

    # 确认
    print("==[info]==📢点击确认按钮, 605 900")
    adb.tap(605, 900)

    print("==[success]==✅退出成功！")
    return True


def login(username, password):
    """登录账号"""
    # todo 检查是否是提示登陆页面
    print("==[info]==📢正在检查是否有提示登录页面")
    # 用百度ocr识别文字“登录后才可获得任务积分奖励”
    ocr_result = ocr.ocr_unlogin_popup()
    if ocr_result:
        # 用返回键关闭弹窗
        adb.back()
    print(f"==[info]==📢准备登录账号：{username}")
    template_paths = [settings.MINE_BTN_PATH, settings.MINE_BTN_02_PATH, settings.MINE_BTN_03_PATH, settings.MINE_BTN_04_PATH]
    x, y, score, path = template_match.find_best_template(adb.screencap(), template_paths)
    if x is not None:
        print(f"==[info]==📢匹配度最高的[我的]按钮：{path}，score={score:.2f}")
        target_x, target_y = x, y
    else:
        print("==[error]==❌ 未找到我的按钮，请检查是否在首页")
        return False
    
    # 打开 “我的”
    mine_success = adb.wait_and_tap("打开我的", 800, 1525,target_x, target_y)
    if not mine_success:
        print("==[ERROR]==❌ 登录失败：打开[我的]失败")
        return False
    #adb.tap(800, 1525)
    # 点击登录
    print("==[info]==📢点击登录按钮, 330 220")
    adb.tap(330, 220)
    # 切换账号密码登录
    template_paths_pwd = [settings.LOGIN_PWD_BTN_PATH]
    x, y, score, path = template_match.find_best_template(adb.screencap(), template_paths_pwd)
    if x is not None:
        print(f"==[info]==📢匹配度最高的[密码登录]按钮：{path}，score={score:.2f}")
        target_x, target_y = x, y
    else:
        print("==[error]==❌ 未找到[密码登录]按钮，请检查是否在登录页面")
        return False
    print("==[info]==📢切换账号密码登录按钮, 100 490")
    pwd_success = adb.wait_and_tap("==[info]==📢切换密码登录", 100, 490,target_x, target_y)
    if not pwd_success:
        print("==[ERROR]==❌ 登录失败：切换密码登录失败")
        return False
    #adb.tap(100, 490)

    # 输入账号
    adb.tap(100, 360)
    adb.input_text(username)

    # 输入密码
    adb.tap(100, 520)
    adb.input_text(password)

    # 点击登录
    adb.tap(450, 650)
    # 点击同意并登录
    print("==[info]==📢点击同意并登录按钮, 605 900")
    adb.tap(605, 900)

    print(f"==[success]==✅ 账号 {username} 登录成功！")
    return True

def switch_to_next_account():
    """从账号列表自动切换到下一个账号"""

    global CURRENT_INDEX

    next_index = (CURRENT_INDEX + 1) % len(ACCOUNTS)
    account = ACCOUNTS[next_index]
    
    print(f"==[info]==📢 切换账号：{CURRENT_INDEX} → {next_index}")

    # 退出
    #logout()
    safe_run(logout, "退出")

    # 登录
    #login(account["username"], account["password"])
    safe_run(lambda: login(account["username"], account["password"]), "登录")

    # 更新索引
    CURRENT_INDEX = next_index

    print(f"==[info]==📢 当前账号已切换为：{account['username']}")

def safe_run(task_fn, name, retries=3):
    for i in range(retries):
        try:
            print(f"==[info]==📢执行 {name}（第 {i+1} 次）")
            success = task_fn()
            if success:
                print(f"✅ {name} 执行成功")
                return True
            print(f"==[error]==❌ {name} 执行失败，重启 App 后重试")
            adb.close_app(settings.DJ_NEWS_PACKAGE)
            adb.open_app(f"{settings.DJ_NEWS_PACKAGE}/{settings.DJ_NEWS_ACTIVITY}")
        except Exception as e:
            print(f"⚠️执行{name} 异常：{e}")
            adb.close_app(settings.DJ_NEWS_PACKAGE)
            adb.open_app(f"{settings.DJ_NEWS_PACKAGE}/{settings.DJ_NEWS_ACTIVITY}")
    print(f"==[error]==❌ 执行{name} 最终失败，跳过")
    return False
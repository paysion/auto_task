import time
import core.adb as adb

# ------------------------------
# 听新闻
# ------------------------------

def task_listen_news():
    print("切换新闻页面")
    adb.tap(90,1550)
    time.sleep(1)
    print("点击听新闻按钮")
    # 固定分辨率，点击100,1425位置为打开听新闻页面
    adb.tap(100, 1425)
    # 450,700为播放按钮位置
    time.sleep(1)
    print("点击播放按钮")
    adb.tap(450,700)
    # 等待一个小时
    time.sleep(3660)

    # --------------------
    # 返回
    # --------------------
    print("听新闻任务结束，返回主界面…")
    adb.cmd("shell input keyevent KEYCODE_BACK")
    time.sleep(1)
    return True

# ------------------------------
# 自动化任务：看直播
# ------------------------------
def task_watch_living_video():
    print("开始执行看直播任务")
    print("点击 450 1550 看视频按钮")
    adb.tap(450, 1550)
    time.sleep(1)
    print("点击 310 85 直播按钮")
    adb.tap(310, 85)
    time.sleep(1)
    # todo 这里的直播可能存在直播结束和直播未开始的情况
    print("点击 450 500 观看直播")
    adb.tap(450, 500)
    # 观看30分钟
    time.sleep(1860)

    # --------------------
    # 返回
    # --------------------
    print("看直播任务结束，返回主界面…")
    adb.cmd("shell input keyevent KEYCODE_BACK")
    time.sleep(1)

    return True

# ------------------------------
# 自动化任务：看视频
# ------------------------------
def task_watch_video():
    print("开始执行看视频任务")
    print("点击 450 1550 看视频按钮")
    adb.tap(450, 1550)
    time.sleep(1)
    print("点击 400 85 切换热点视频")
    adb.tap(400, 85)
    time.sleep(1)
    # todo 怎么确定每个视频的时间长短，目前是固定每过60秒滑一个
    for i in range(20):
        print(f"正在滑动第 {i+1}/10 个视频")
        adb.swipe(450, 800, 450, 500, 300)
        time.sleep(60)

    # --------------------
    # 返回
    # --------------------
    print("看视频任务结束…")
    time.sleep(1)

    return True

# ------------------------------
# 自动化任务：看新闻
# ------------------------------
def task_watch_news():
    print("开始执行看新闻任务")
    print("点击 90 1550 看新闻按钮")
    adb.tap(90, 1550)
    time.sleep(1)
    print("点击 300 130 看热榜")
    adb.tap(300, 130)
    time.sleep(1)
    for i in range(7):
        # 7个新闻，每次y轴加100像素看下一个
        print("新闻坐标",450,410 + i*99)
        adb.tap(450,410 + i*99)
        print(f"正在观看第 {i+1}/10 个新闻")
        # 滑动观看新闻
        for _ in range(6):
            adb.human_swipe()
        # todo 添加评论
        # 识别新闻标题
        # screen = adb_screencap()
        # 添加ocr识别新闻标题
        # comment = gen_comment(text)
        adb.swipe(450, 800, 450, 300, 300)
        time.sleep(1)
        adb.cmd("shell input keyevent KEYCODE_BACK")
        time.sleep(1)



# ------------------------------
# 主流程
# ------------------------------
def run_tasks():
    print(">>> 开始执行每日积分任务 <<<")

    success = task_watch_news()
    time.sleep(10)

    #success = task_watch_video()
    #time.sleep(10)

    #success = task_watch_living_video()
    #time.sleep(10)

    #success = task_listen_news()

    print(">>> 积分任务执行结束 <<<")


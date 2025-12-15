import time
import core.adb as adb
import core.ocr as ocr
import core.comment as comment
import core.template_match as template_match
import utils.image_utils as image_utils
import config.settings as settings
import random
import utils.chrome_utils as chrome_utils

# ------------------------------
# 听新闻
# ------------------------------
def task_listen_news():
    print(">>> 开始听新闻 <<<")
    
    print("切换新闻页面")
    adb.tap(90,1550)
    
    print("点击听新闻按钮 70 1440")
    adb.tap(70, 1440)
    
    print("点击播放按钮 450 700")
    adb.tap(450,700)
    # 任务听完一个小时
    time.sleep(3660)

    print("======听新闻任务结束，返回主界面…=======")
    adb.back()

# ------------------------------
# 自动化任务：看直播
# ------------------------------
def task_watch_living_video():
    print(">>> 开始执行看直播任务 <<<")
    
    print("点击 450 1550 看视频按钮")
    adb.tap(450, 1550)
    
    print("点击 310 85 直播按钮")
    adb.tap(310, 85)
    # 模板匹配正在直播或者直播回顾的按钮
    success = find_and_tap_live_button()
    if success:
        # 观看30分钟
        time.sleep(1860)
        print("点击 857 98 退出直播")
        adb.tap(857, 98)
        print("======看直播任务结束……======")
        return True
    else:
        print("======看直播任务失败……======")
        return False


def find_and_tap_live_button(max_attempts=3):
    """
    尝试在屏幕上匹配 live 按钮（包括正在直播和直播回顾），找到则点击。
    匹配失败会下滑重试，最多重试 max_attempts 次。
    """
    for attempt in range(1, max_attempts + 1):
        print(f"第 {attempt} 次尝试匹配按钮...")

        # 截图一次以提高效率
        screen = adb.screencap()

        # 匹配两个模板
        x1, y1, _ = template_match.find_template(screen, settings.LIVING_VIDEO_BTN_PATH)
        x2, y2, _ = template_match.find_template(screen, settings.LIVE_VIDEO_BTN_PATH)

        # 模板1匹配成功
        if x1 is not None and y1 is not None:
            print(f"匹配到 LIVING_VIDEO_BTN，位置: ({x1}, {y1})")
            adb.tap(x1, y1)
            return True

        # 模板2匹配成功
        if x2 is not None and y2 is not None:
            print(f"匹配到 LIVE_VIDEO_BTN，位置: ({x2}, {y2})")
            adb.tap(x2, y2)
            return True

        # 两个模板都没匹配成功 → 下滑继续找
        if attempt < max_attempts:
            print("未找到按钮，下滑重新尝试...")
            adb.swipe(450, 1225, 450, 500, 300)
        else:
            print("连续尝试均失败，未找到任何直播按钮！")
            return False

# ------------------------------
# 看视频
# ------------------------------
def task_watch_video():
    print(">>> 开始看视频 <<<")
    
    print("点击 450 1550 看视频按钮")
    adb.tap(450, 1550)
    
    print("点击 400 85 切换热点视频")
    adb.tap(400, 85)
    
    # todo 怎么确定每个视频的时间长短，目前是固定每过60秒滑一个
    driver = chrome_utils.create_chrome_driver()
    try:
        for i in range(12):
            print(f"正在滑动第 {i+1}/12 个视频")
            adb.swipe(450, 800, 450, 500, 300)

            print("点击 840 1350 分享按钮")
            adb.tap(840, 1350)

            print("点击 100 1380 复制链接")
            adb.tap(100, 1380)

            url = adb.get_clipboard()
            print("打开分享链接", url)

            chrome_utils.chrome_open(driver, url)

            time.sleep(random.uniform(40, 60))

    finally:
        # 确保最终一定释放资源
        driver.quit()  
        #print("分享任务完成！")
    print("======看视频任务结束……======")

# ------------------------------
# 自动化任务：看新闻
# ------------------------------
def task_watch_news():
    print(">>> 开始看新闻 <<<")
   
    print("点击 90 1550 看新闻按钮")
    adb.tap(90, 1550)
   
    print("点击 380 175 看热榜")
    adb.tap(380, 175)
    
    for i in range(7):
        # 7个新闻，每次y轴加99像素看下一个
        print("新闻坐标",450,410 + i*99)
        adb.tap(450,410 + i*99)
        print(f"正在观看第 {i+1}/7 个新闻")
        
        # 生成评论
        image = adb.screencap()
        image_bytes = image_utils.encode_png(image)
        res_ocr = ocr.ocr_image(image_bytes)
        res_comment = comment.gen_comment(res_ocr)
        time.sleep(5)
        
        # 滑动观看新闻
        for _ in range(4):
            adb.human_swipe()
        print("点击 100 1560添加评论")
        adb.tap(100, 1560)
        adb.input_text(res_comment)
        print("点击 820 1500发送")
        adb.tap(820, 1500)
        
        adb.back()
    print("======看新闻任务结束……======")


# ------------------------------
# 主流程
# ------------------------------
def run_tasks():
    print(">>> 开始执行每日积分任务 <<<")

    # 看视频
    task_watch_video()
    time.sleep(10)

    # 看新闻
    task_watch_news()
    time.sleep(10)
    
    # 听新闻
    task_listen_news()
    time.sleep(10)

    # 看直播
    task_watch_living_video()
    time.sleep(10)

    print(">>> 积分任务执行结束 <<<")


import time
import core.adb as adb
import core.ocr as ocr
import core.comment as comment
import core.template_match as template_match
import utils.image_utils as image_utils
import config.settings as settings
import random
import utils.chrome_utils as chrome_utils
import config.settings as settings

# ------------------------------
# 听新闻
# ------------------------------
def task_listen_news(task_seconds=3660):
    print(">>> 🎧 开始执行【听新闻】任务，检查是否在新闻页面 <<<")
    news_btn_paths = [
        settings.NEWS_BTN_PATH,
        settings.NEWS_BTN_02_PATH,
        settings.NEWS_BTN_03_PATH,
    ]
    x, y, _, _ = template_match.find_best_template(adb.screencap(), news_btn_paths)
    if x is None:
        print("==[error]==❌ 未找到[新闻]按钮，请检查是否在首页")
        return False
    success = adb.wait_and_tap("看新闻", 90, 1550,x, y)
    if not success:
        print("==[error]==❌ 不在新闻页面，请检查是否在看新闻页面")
        return False
    #print("切换新闻页面")
    #adb.tap(90,1550)
    
    print("==[info]==📢点击听新闻按钮 70 1440")
    adb.tap(70, 1440)
    
    x1, y1, _ = template_match.find_template(adb.screencap(), settings.LISTEN_PLAY_BTN_PATH,0.9)
    if x1 is None:
        print("==[error]==❌ 未找到[播放]按钮，播放新闻失败！")
        return False
    listen_success = adb.wait_and_tap("播放新闻", 450, 700, x1, y1)
    if not listen_success:
        print("==[error]==❌ 播放新闻失败！")
        return False 
    
    # print("📢点击播放按钮 450 700")
    # adb.tap(450,700)
    
    # 任务听完一个小时
    time.sleep(task_seconds)
    # 检查是否完成任务
    status, remain = ocr.ocr_minutes()
    if status == "unknown":
        print("==[error]==❌ 未识别到听新闻分钟数！")
        #adb.back()
        return False
    elif status == "done":
        print("======✅听新闻任务结束，返回主界面=======")
        adb.back()
        return True
    elif status == "ing":
        print("======听新闻任务正在进行中=======")
        # time.sleep(remain*60)
        # 预留 5 秒缓冲，避免刚好卡在 60 分钟边界
        sleep_seconds = max(remain * 60 + 5, 10)
        print(f"==[info]==⏳等待 {sleep_seconds} 秒后重新识别")
        time.sleep(sleep_seconds)

        # 再次校验是否完成
        for i in range(3):  # 最多重试 3 次
            print(f"==[info]==📢 第 {i + 1} 次重新识别听新闻状态")
            status2, _ = ocr.ocr_minutes()

            if status2 == "done":
                print("======✅听新闻任务确认完成，返回主界面=======")
                adb.back()
                return True

            if status2 == "unknown":
                print("==[warn]==⚠️ OCR 识别失败，等待 5 秒重试")
                time.sleep(5)
                continue

            print("==[info]==📢 听新闻仍未完成，继续等待 10 秒")
            time.sleep(10)

        print("==[error]==❌ 多次确认后仍未完成听新闻任务")
        return False
    
    print("==[error]==❌ 【听新闻】任务发生未知状态")
    return False

# ------------------------------
# 自动化任务：看直播
# ------------------------------
def task_watch_living_video():
    print(">>> 开始执行看直播任务，检查是否在视频页面 <<<")
    x, y, _ = template_match.find_template(adb.screencap(), settings.VIDEO_BTN_PATH)
    success = adb.wait_and_tap("==[info]==📢看视频", 450, 1550,x, y)
    if not success:
        print("==[error]==❌ 不在视频页面，请检查是否在看视频页面")
        return False
    #print("点击 450 1550 看视频按钮")
    #adb.tap(450, 1550)
    
    print("点击 310 85 直播按钮")
    adb.tap(310, 85)
    # 模板匹配正在直播或者直播回顾的按钮
    success = find_and_tap_live_button()
    if success:
        # 观看30分钟
        time.sleep(1860)
        print("点击 857 98 退出直播")
        adb.tap(857, 98)
        print("======✅看直播任务结束======")
        return True
    else:
        print("======❌看直播任务失败======")
        return False


def find_and_tap_live_button(max_attempts=3):
    """
    尝试在屏幕上匹配 live 按钮（包括正在直播和直播回顾），找到则点击。
    匹配失败会下滑重试，最多重试 max_attempts 次。
    """
    for attempt in range(1, max_attempts + 1):
        print(f"==[info]==📢第 {attempt} 次尝试匹配按钮...")

        # 截图一次以提高效率
        screen = adb.screencap()

        # 匹配两个模板
        x1, y1, _ = template_match.find_template(screen, settings.LIVING_VIDEO_BTN_PATH)
        x2, y2, _ = template_match.find_template(screen, settings.LIVE_VIDEO_BTN_PATH)

        # 模板1匹配成功
        if x1 is not None and y1 is not None:
            print(f"==[info]==📢匹配到 LIVING_VIDEO_BTN，位置: ({x1}, {y1})")
            adb.tap(x1, y1)
            return True

        # 模板2匹配成功
        if x2 is not None and y2 is not None:
            print(f"==[info]==📢匹配到 LIVE_VIDEO_BTN，位置: ({x2}, {y2})")
            adb.tap(x2, y2)
            return True

        # 两个模板都没匹配成功 → 下滑继续找
        if attempt < max_attempts:
            print("==[info]==⚠️ 未找到按钮，下滑重新尝试...")
            adb.swipe(450, 1225, 450, 500, 300)
        else:
            print("==[error]==❌连续尝试均失败，未找到任何直播按钮！")
            return False

# ------------------------------
# 看视频
# ------------------------------
def task_watch_video():
    print(">>> 开始看视频，检查是否在视频页面 <<<")
    x, y, _ = template_match.find_template(adb.screencap(), settings.VIDEO_BTN_PATH)
    success = adb.wait_and_tap("看视频", 450, 1550,x, y)
    #print("点击 450 1550 看视频按钮")
    #adb.tap(450, 1550)
    if not success:
        print("==[error]==❌ 不在视频页面，请检查是否在看视频页面")
        return False
    print("==[info]==📢点击 400 85 切换热点视频")
    adb.tap(400, 85)
    
    # todo 怎么确定每个视频的时间长短，目前是固定每过60秒滑一个
    for i in range(12):
            print(f"==[info]==📢正在滑动第 {i+1}/12 个视频")
            adb.swipe(450, 800, 450, 500, 300)

            print("==[info]==📢点击 840 1350 分享按钮")
            adb.tap(840, 1350)

            print("==[info]==📢点击 100 1380 复制链接")
            adb.tap(100, 1380)

            url = adb.get_clipboard()
            print("==[info]==📢打开分享链接", url)
            if not url.startswith("https://dj.jxnews.com.cn/"):
                print("==[error]==❌ 分享链接无效")
                adb.back()
                continue
            adb.open_url(url)
            adb.back()

            time.sleep(random.uniform(40, 60))

    print("======✅看视频任务结束……======")
    return True

# ------------------------------
# 自动化任务：看新闻
# ------------------------------
def task_watch_news():
    print(">>> 开始看新闻，检查是否在新闻页面 <<<")
    news_btn_paths = [settings.NEWS_BTN_02_PATH, settings.NEWS_BTN_PATH]
    x, y, score, path = template_match.find_best_template(adb.screencap(), news_btn_paths)
    if x is not None:
        print(f"==[info]==📢匹配度最高的新闻按钮：{path}，score={score:.2f}")
    else:
        print("==[error]==❌ 未找到新闻按钮，请检查是否在新闻页面")
        return False
    
    success = adb.wait_and_tap("看新闻", 90, 1550,x, y)
    if not success:
        print("==[error]==❌ 不在新闻页面，请检查是否在看新闻页面")
        return False
    #print("点击 90 1550 看新闻按钮")
    #adb.tap(90, 1550)
   
    print("==[info]==📢点击 380 175 看热榜")
    adb.tap(380, 175)
    
    for i in range(7):
        # 7个新闻，每次y轴加99像素看下一个
        print("==[info]==📢新闻坐标",450,410 + i*99)
        adb.tap(450,410 + i*99+99)
        print(f"==[info]==📢正在观看第 {i+1}/7 个新闻")
        
        # 生成评论
        image = adb.screencap()
        image_bytes = image_utils.encode_png(image)
        res_ocr = ocr.ocr_image(image_bytes)
        res_comment = comment.gen_comment(res_ocr)
        if res_comment == "unknown":
            print("==[error]==❌ 调用deepseek评论生成失败")
            return False
        time.sleep(5)
        
        # 滑动观看新闻
        for _ in range(4):
            adb.human_swipe()
        print("==[info]==📢点击 100 1560添加评论")
        adb.tap(100, 1560)
        adb.input_text(res_comment)
        print("==[info]==📢点击 820 1490发送")
        adb.tap(820, 1490)
        
        adb.back()
    
    print("======✅看新闻任务结束……======")
    return True


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


# ------------------------------
# 主流程
# ------------------------------
def run_tasks():
    print(">>> 开始执行每日积分任务 <<<")

    # 看视频
    #task_watch_video()
    safe_run(task_watch_video, "看视频")
    time.sleep(10)

    # 看新闻
    # task_watch_news()
    safe_run(task_watch_news, "看新闻")
    time.sleep(10)
    
    # 听新闻
    # task_listen_news()
    safe_run(task_listen_news, "听新闻")
    time.sleep(10)

    # 看直播
    # task_watch_living_video()
    safe_run(task_watch_living_video, "看直播")
    time.sleep(10)

    print(">>> 积分任务执行结束 <<<")


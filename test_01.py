from pywinauto import Application,Desktop
import random
import subprocess
import cv2
import numpy as np
import time
import schedule
import requests
from openai import OpenAI
import os


DEVICE = "127.0.0.1:5555"


# ------------------------------
# ADB 工具函数
# ------------------------------

def adb_cmd(cmd):
    """ 执行 adb 命令 """
    return subprocess.run(f"adb -s {DEVICE} {cmd}", shell=True)
def adb_screencap():
    """ 截图并返回 OpenCV 图片 """
    p = subprocess.Popen(
        f"adb -s {DEVICE} exec-out screencap -p",
        shell=True, stdout=subprocess.PIPE
    )
    data = p.stdout.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    return img

def adb_tap(x, y):
    """ 点击屏幕 """
    adb_cmd(f"shell input tap {x} {y}")

def adb_swipe(x1, y1, x2, y2, duration=300):
    """ 滑动 """
    adb_cmd(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")

# ------------------------------
# 模板匹配工具
# ------------------------------

def find_template(screen, template_path, threshold=0.8):
    tpl = cv2.imread(template_path)
    # 获取模板图片的宽高
    h, w = tpl.shape[:2]

    result = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    x = max_loc[0] + w//2
    y = max_loc[1] + h//2
    return x, y, max_val

# ------------------------------
# 自动化任务：听新闻示例
# ------------------------------

def task_listen_news():
    # print("正在截屏...")
    # screen = adb_screencap()
    # 将图片保存template/screenshots目录下
    # cv2.imwrite(f"templates/screenshots/listen_news_{time.time()}.png", screen)
    #print("正在查找『听新闻』按钮...")
    #pos = find_template(screen, "templates/listen_news_btn.png", 0.75)
    # if not pos:
    #     print("未找到『听新闻』按钮，可能需要滑动页面。")
    #     return False
    # x, y, score = pos
    # print(f"找到按钮！匹配度={score:.2f} 坐标=({x}, {y})")
    # adb_tap(x, y)
    # print("已点击，正在进入听新闻页面...")
    # time.sleep(2)

    print("切换新闻页面")
    adb_tap(90,1550)
    time.sleep(1)
    print("点击听新闻按钮")
    # 固定分辨率，点击100,1425位置为打开听新闻页面
    adb_tap(100, 1425)
    # 450,700为播放按钮位置
    time.sleep(1)
    print("点击播放按钮")
    adb_tap(450,700)
    # 等待一个小时
    time.sleep(3660)

    # --------------------
    # 返回
    # --------------------
    print("听新闻任务结束，返回主界面…")
    adb_cmd("shell input keyevent KEYCODE_BACK")
    time.sleep(1)
    return True

# ------------------------------
# 自动化任务：看直播
# ------------------------------
def task_watch_living_video():
    print("开始执行看直播任务")
    print("点击 450 1550 看视频按钮")
    adb_tap(450, 1550)
    time.sleep(1)
    print("点击 310 85 直播按钮")
    adb_tap(310, 85)
    time.sleep(1)
    # todo 这里的直播可能存在直播结束和直播未开始的情况
    print("点击 450 500 观看直播")
    adb_tap(450, 500)
    # 观看30分钟
    time.sleep(1860)

    # --------------------
    # 返回
    # --------------------
    print("看直播任务结束，返回主界面…")
    adb_cmd("shell input keyevent KEYCODE_BACK")
    time.sleep(1)

    return True

# ------------------------------
# 自动化任务：看视频
# ------------------------------
def task_watch_video():
    print("开始执行看视频任务")
    print("点击 450 1550 看视频按钮")
    adb_tap(450, 1550)
    time.sleep(1)
    print("点击 400 85 切换热点视频")
    adb_tap(400, 85)
    time.sleep(1)
    # todo 怎么确定每个视频的时间长短，目前是固定每过60秒滑一个
    for i in range(20):
        print(f"正在滑动第 {i+1}/10 个视频")
        adb_swipe(450, 800, 450, 500, 300)
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
    adb_tap(90, 1550)
    time.sleep(1)
    print("点击 300 130 看热榜")
    adb_tap(300, 130)
    time.sleep(1)
    for i in range(10):
        # 10个新闻，每次y轴加100像素看下一个
        print("新闻坐标",450,410 + i*99)
        adb_tap(450,410 + i*99)
        print(f"正在观看第 {i+1}/10 个新闻")
        # 滑动观看新闻
        for _ in range(6):
            human_swipe()
        # todo 添加评论
        # 识别新闻标题
        # screen = adb_screencap()
        # 添加ocr识别新闻标题
        # comment = gen_comment(text)
        adb_swipe(450, 800, 450, 300, 300)
        time.sleep(1)
        adb_cmd("shell input keyevent KEYCODE_BACK")
        time.sleep(1)


def human_swipe():
    start_y = random.randint(1200, 1500)
    end_y = random.randint(300, 500)
    duration = random.randint(250, 380)

    adb_swipe(500, start_y, 500, end_y, duration)
    time.sleep(random.uniform(0.8, 1.4))

def gen_comment(text):
    """
    根据新闻内容 / 视频标题生成评论
    """
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

    prompt = f"请根据下面内容生成一条简短自然的评论，要求内容积极向上，不要出现政治内容，20字左右：\n{text}"
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个新闻读者"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content



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



# ------------------------------
# 定时任务设置：每天 09:00 自动运行
# ------------------------------
if __name__ == "__main__":
    print(">>> 大江新闻自动积分系统已启动（将每日 09:00 自动刷积分） <<<")

    # schedule.every().day.at("09:00").do(run_tasks)
    run_tasks()
    # 无限循环，随时等待任务触发
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


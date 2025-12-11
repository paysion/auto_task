import subprocess
import cv2
import numpy as np
import random
import time
from config.settings import DEVICE

def cmd(cmd):
    return subprocess.run(f"adb -s {DEVICE} {cmd}", shell=True)

# 点击
def tap(x, y):
    cmd(f"shell input tap {x} {y}")
    # 点击后延迟1秒
    time.sleep(random.uniform(2, 3))

# 滑动
def swipe(x1, y1, x2, y2, duration=300):
    cmd(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
    # 点击后延迟1秒
    time.sleep(random.uniform(0.8, 1.4))

# 截图
def screencap_cv2():
    """返回OpenCV格式截图"""
    p = subprocess.Popen(
        f"adb -s {DEVICE} exec-out screencap -p",
        shell=True, stdout=subprocess.PIPE
    )
    data = p.stdout.read()
    return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

def screencap():
    """ 使用ADB对设备截图并返回OpenCV图像 """
    try:
        p = subprocess.Popen(
            f"adb -s {DEVICE} exec-out screencap -p",
            shell=True,
            stdout=subprocess.PIPE
        )
        data = p.stdout.read()

        if not data:
            raise RuntimeError("未读取到截图数据")

        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        raise RuntimeError(f"[ERROR] 截图失败：{e}")

# 模拟真实人类滑动
def human_swipe():
    start_y = random.randint(1200, 1500)
    end_y = random.randint(300, 500)
    duration = random.randint(250, 380)

    swipe(500, start_y, 500, end_y, duration)
    time.sleep(random.uniform(0.8, 1.4))

# 输入文字
def input_text(text):
    """
    向安卓设备输入文字
    """
    adb_cmd = f'shell input text {text}'
    cmd(adb_cmd)
    time.sleep(random.uniform(2, 3))

# 返回
def back():
    """
    返回
    """
    cmd(f'shell input keyevent KEYCODE_BACK')
    time.sleep(random.uniform(0.8, 1.4))
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

# 滑动
def swipe(x1, y1, x2, y2, duration=300):
    cmd(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")

# 截图
def screencap_cv2():
    """返回OpenCV格式截图"""
    p = subprocess.Popen(
        f"adb -s {DEVICE} exec-out screencap -p",
        shell=True, stdout=subprocess.PIPE
    )
    data = p.stdout.read()
    return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

# 模拟真实人类滑动
def human_swipe():
    start_y = random.randint(1200, 1500)
    end_y = random.randint(300, 500)
    duration = random.randint(250, 380)

    swipe(500, start_y, 500, end_y, duration)
    time.sleep(random.uniform(0.8, 1.4))
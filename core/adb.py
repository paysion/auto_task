import subprocess
import cv2
import numpy as np
import random
import time
import pyperclip
import urllib.parse
from config.settings import DEVICE
import math


def cmd(cmd):
    return subprocess.run(f"adb -s {DEVICE} {cmd}", shell=True)

# 点击
def tap(x, y):
    cmd(f"shell input tap {x} {y}")
    # 点击后延迟1秒
    print(f">>> [adb shell]: adb -s {DEVICE} shell input tap {x} {y}")
    time.sleep(random.uniform(3, 4))

# 滑动
def swipe(x1, y1, x2, y2, duration=300):
    cmd(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
    # 点击后延迟1秒
    print(f">>> [adb shell]: adb -s {DEVICE} shell input swipe {x1} {y1} {x2} {y2} {duration}")
    time.sleep(random.uniform(1, 2))

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
    print(f">>> [adb shell]: adb -s {DEVICE} shell input keyevent KEYCODE_BACK")
    time.sleep(random.uniform(1, 2))

# 获取剪切板
def get_clipboard():
    """
    直接获取PC剪贴板内容（MuMu与PC共享剪贴板）
    """
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"[ERROR] 获取剪贴板失败: {e}")
        return ""

# 打开分享链接    
def open_url(url):
    """使用 ADB 打开链接"""
    # 检查url是否是https://dj.jxnews.com.cn/开头的
    
    encoded = urllib.parse.quote(url, safe=":/?&=")
    adb_cmd = f'shell am start -a android.intent.action.VIEW -d \\"{encoded}\\""'
    cmd(adb_cmd)
    print(f">>> [adb shell]: adb -s {DEVICE} {adb_cmd}")
    time.sleep(5)

# 等待并校验
def wait_and_tap(desc, x, y, x0, y0, timeout=15, threshold=30):
    """
    等待并点击
    :param desc: 描述
    :param x: x坐标
    :param y: y坐标
    :param x0: 匹配的x坐标
    :param y0: 匹配的y坐标
    :param timeout: 超时时间
    :return: 是否成功
    """
    start = time.time()
    while time.time() - start < timeout:
        print(f"==[info]==📢准备点击 {x} {y} {desc}")
        tap(x, y)
        # 计算两点之间的欧几里得距离,相差不大（阈值默认20）则认为比对成功
        distance = math.hypot(x - x0, y - y0)
        print(f"==[info]==📢检验欧几里得距离: {distance}")
        if distance <= threshold:
            print(f"==[success]== ✅{desc} 成功")
            time.sleep(random.uniform(2, 3))
            return True
    print(f"==[error]== ❌{desc} 失败（超时）")
    return False

# 打开应用 adb -s 127.0.0.1:5555 shell am start -n 
# com.jxnews.jxttn/com.zjonline.xsb_main.MainAliasActivity.MainAliasActivityDefault
def open_app(package_name):
    """
    打开应用
    :param package_name: 包名
    """
    cmd(f'shell am start -n {package_name}')
    print(f">>> [adb shell]: adb -s {DEVICE} shell am start -n {package_name}")
    time.sleep(15)

# 关闭应用 adb -s 127.0.0.1:5555 shell am force-stop com.jxnews.jxttn
def close_app(package_name):
    """
    关闭应用
    :param package_name: 包名
    """
    cmd(f'shell am force-stop {package_name}')
    print(f">>> [adb shell]: adb -s {DEVICE} shell am force-stop {package_name}")
    time.sleep(5)
import subprocess
import time
from PIL import Image
import numpy as np
import cv2


def adb(cmd):
    return subprocess.getoutput(f"adb {cmd}")


def tap(x, y):
    adb(f"shell input tap {x} {y}")


def swipe(x1, y1, x2, y2, duration=300):
    adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")


def screenshot():
    """
    截图 → 返回 OpenCV 格式图片
    """
    adb("shell screencap -p /sdcard/tmp.png")
    adb("pull /sdcard/tmp.png ./screen.png")
    img = cv2.imread("./screen.png")
    return img

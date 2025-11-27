import pyautogui
import time
import numpy as np
from PIL import ImageGrab

# -------------------------------
# 屏幕截图
# -------------------------------
def screenshot():
    """
    截取全屏，返回 OpenCV 格式的图片
    """
    img = ImageGrab.grab()
    img = np.array(img)
    img = img[:, :, ::-1]  # RGB → BGR (OpenCV格式)
    return img


# -------------------------------
# 鼠标点击
# -------------------------------
def click(x, y):
    """
    移动鼠标到(x,y) 并点击
    """
    pyautogui.moveTo(x, y, duration=0.15)
    pyautogui.click()
    print(f"[点击] ({x}, {y})")


# -------------------------------
# 下滑滚动
# -------------------------------
def scroll_down(pixels=800):
    """
    模拟鼠标下滑滚动
    """
    pyautogui.scroll(-pixels)
    print("[滚动] 页面下拉")
    time.sleep(1)

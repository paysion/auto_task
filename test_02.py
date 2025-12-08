from pywinauto import Application,Desktop
import pyautogui
import cv2
import numpy as np
import time

# 1. 找到记事本窗口
window = Desktop(backend="win32").window(title_re=".*记事本.*")
# 恢复窗口
window.restore()   
window.set_focus()

print("窗口找到！")

# 2. 获取窗口坐标
rect = window.rectangle()
left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
width = right - left
height = bottom - top

print("记事本", left, top, width, height)

# 3. 截图窗口内容
img = pyautogui.screenshot(region=(left, top, width, height))
img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# 4. 加载模板图片（例如 “我的” 按钮）
template = cv2.imread("templates/help.png")

# 5. 模板匹配
res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

print("匹配度：", max_val)

if max_val > 0.8:
    # 6. 找到按钮中心坐标（映射到屏幕坐标）
    h, w = template.shape[:2]
    center_x = left + max_loc[0] + w // 2
    center_y = top + max_loc[1] + h // 2

    print("按钮坐标：", center_x, center_y)
    time.sleep(1)
    # 7. 点击该坐标 fixme 这里点击为什么没生效，但是输出了“按钮已点击”
    pyautogui.click(center_x, center_y, duration=0.5)
    print("按钮已点击！")
else:
    print("未找到按钮")


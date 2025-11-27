import numpy as np
from paddleocr import PaddleOCR
from control import screenshot


# 初始化 OCR（中文）
ocr = PaddleOCR(use_angle_cls=True, lang='ch')


# -----------------------------------
# 模板匹配（找按钮图）
# -----------------------------------
def find_template(template_path, threshold=0.8):
    """
    用 OpenCV 在屏幕中查找模板图片的位置
    返回按钮中心坐标 (x, y)
    """
    screen = screenshot()
    tpl = cv2.imread(template_path)

    res = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = tpl.shape[:2]
        x = max_loc[0] + w // 2
        y = max_loc[1] + h // 2
        print(f"[模板匹配] 找到 {template_path}")
        return (x, y)

    return None


# -----------------------------------
# OCR 查找文字
# -----------------------------------
def find_text(keywords):
    """
    OCR 在屏幕中查找关键文字，返回中心坐标
    keywords = ["未完成"]
    """
    screen = screenshot()
    result = ocr.ocr(screen, cls=True)

    for line in result:
        box = line[0]  # 文本区域四边形
        text = line[1][0]

        # 如果检测到关键字
        if any(k in text for k in keywords):
            x = int((box[0][0] + box[2][0]) / 2)
            y = int((box[0][1] + box[2][1]) / 2)
            print(f"[OCR] 找到文字：{text}")
            return (x, y)

    return None

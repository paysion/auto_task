import cv2
import numpy as np
from paddleocr import PaddleOCR


ocr = PaddleOCR(use_angle_cls=True, lang='ch')


def match_template(screen, tpl_path, threshold=0.85):
    tpl = cv2.imread(tpl_path)
    res = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        x, y = max_loc
        h, w = tpl.shape[:2]
        return (x + w//2, y + h//2)
    return None


def find_text(screen, keywords):
    """
    OCR 查找指定文字
    """
    result = ocr.ocr(screen, cls=True)
    for line in result:
        for text, box in [(line[1][0], line[0])]:
            if any(k in text for k in keywords):
                # box: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                x = int((box[0][0] + box[2][0]) / 2)
                y = int((box[0][1] + box[2][1]) / 2)
                return (x, y)
    return None

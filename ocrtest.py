from paddleocr import PaddleOCR
import cv2
import numpy as np
import subprocess
import time

# 初始化 OCR（只需一次）
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

DEVICE = "127.0.0.1:5555"

def adb_screencap():
    """ 使用 ADB 截图并返回 OpenCV 图像 """
    p = subprocess.Popen(
        f"adb -s {DEVICE} exec-out screencap -p",
        shell=True,
        stdout=subprocess.PIPE
    )
    data = p.stdout.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    return img

def extract_text_from_result(result):
    """
    适配你当前 OCR 的 result（paddleX OCR），
    自动从 result[0]["rec_texts"] 获取所有文本。
    """
    if isinstance(result, list) and len(result) > 0:
        item = result[0]

        # rec_texts 存在
        if isinstance(item, dict) and "rec_texts" in item:
            return "\n".join(item["rec_texts"])

    return ""   # 未识别出文本


def ocr_screen():
    """ 对当前屏幕执行 OCR，返回文字 """
    # 从template/screenshots目录下截屏
    # img = cv2.imread(f"templates/screenshots/watch_news_202512081011.png")
    img = adb_screencap()
    # OCR 识别
    result = ocr.predict(img)
    # 解析文本
    text = extract_text_from_result(result)
    return text


# 测试
if __name__ == "__main__":
    print("正在执行 OCR...")
    text = ocr_screen()
    print("识别结果：")
    print(text)

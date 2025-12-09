import cv2
import numpy as np
import subprocess
import requests
import base64
import time
import re

# ===============================
# 百度 OCR 配置
# ===============================
API_KEY = "Wnl3lfYyjcdQyh8I8PRF4qYx"
SECRET_KEY = "HXZFSYEs7D6w4lwC4v3kO0lEI2b0CH2A"
DEVICE = "127.0.0.1:5555"

TOKEN_CACHE = None
TOKEN_EXPIRE_TIME = 0


# ===============================
# 获取百度OCR access_token（含缓存）
# ===============================
def get_access_token():
    global TOKEN_CACHE, TOKEN_EXPIRE_TIME

    # 如果缓存有效，直接返回
    if TOKEN_CACHE and time.time() < TOKEN_EXPIRE_TIME:
        return TOKEN_CACHE

    print("[INFO] 正在获取新的 access_token...")

    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }

    try:
        res = requests.get(url, params=params).json()
        if "access_token" not in res:
            raise Exception("获取 token 失败：" + str(res))

        TOKEN_CACHE = res["access_token"]
        TOKEN_EXPIRE_TIME = time.time() + int(res["expires_in"]) - 60  # 提前60秒刷新
        return TOKEN_CACHE

    except Exception as e:
        raise RuntimeError(f"[ERROR] 获取 access_token 失败: {e}")


# ===============================
# OCR 调用
# ===============================
def baidu_ocr(image_bytes):
    """ 调用百度OCR识别图像（输入：bytes） """
    token = get_access_token()
    ocr_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}"

    img_base64 = base64.b64encode(image_bytes)

    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"image": img_base64}

    try:
        res = requests.post(ocr_url, data=data, headers=headers).json()
        return res
    except Exception as e:
        raise RuntimeError(f"[ERROR] OCR 请求失败: {e}")


# ===============================
# OCR 结果清洗 + 自动修复换行
# ===============================
def clean_ocr_result(ocr_json):
    if "words_result" not in ocr_json:
        return ""

    lines = []
    for item in ocr_json["words_result"]:
        txt = item["words"].strip()

        # 去掉单独符号或无意义内容
        if len(txt) <= 2 and re.match(r'^[^\u4e00-\u9fa5a-zA-Z0-9]+$', txt):
            continue

        lines.append(txt)

    # 自动合并句子（尽量恢复正常段落）
    final_text = ""
    for i, line in enumerate(lines):
        if final_text and not final_text.endswith(("。", "！", "？")):
            final_text += line
        else:
            final_text += ("\n" if i > 0 else "") + line

    return final_text.strip()


# ===============================
# ADB 截屏
# ===============================
def adb_screencap():
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


# ===============================
# 屏幕 OCR 主流程
# ===============================
def ocr_screen():
    """ 截图并执行 OCR，返回文本 """
    img = adb_screencap()

    # 编码为 PNG 二进制
    _, encoded_img = cv2.imencode(".png", img)
    image_bytes = encoded_img.tobytes()

    ocr_json = baidu_ocr(image_bytes)
    text = clean_ocr_result(ocr_json)
    return text


# ===============================
# 本地图片 OCR
# ===============================
def ocr_local_image(path):
    with open(path, "rb") as f:
        image_bytes = f.read()

    ocr_json = baidu_ocr(image_bytes)
    return clean_ocr_result(ocr_json)


# ===============================
# 测试入口
# ===============================
if __name__ == "__main__":
    print("正在执行 OCR...")

    # 测试本地图片
    # text = ocr_local_image("templates/screenshots/watch_news_202512081011.png")

    # 测试 ADB 截图
    text = ocr_screen()

    print("\n识别结果：\n")
    print(text)

import requests
import base64
import time
import utils.text_utils as text_utils
from config.settings import API_KEY, SECRET_KEY
import utils.image_utils as image_utils
import core.adb as adb

TOKEN_CACHE = None
TOKEN_EXPIRE = 0

def get_token():
    global TOKEN_CACHE, TOKEN_EXPIRE

    if TOKEN_CACHE and time.time() < TOKEN_EXPIRE:
        return TOKEN_CACHE

    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }

    res = requests.get(url, params=params).json()
    TOKEN_CACHE = res["access_token"]
    TOKEN_EXPIRE = time.time() + res["expires_in"] - 60
    return TOKEN_CACHE

def ocr_image(image_bytes):
    token = get_token()
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}"

    img_b64 = base64.b64encode(image_bytes)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"image": img_b64}

    res = requests.post(url, data=data, headers=headers).json()
    return text_utils.clean_ocr_text(res)

# 识别听新闻的分钟数
def ocr_minutes():
    """
    unknown表示未识别，done表示已完成，ing表示正在进行
    """
    image = adb.screencap()
    image_bytes = image_utils.encode_png(image)
    res_ocr = ocr_image(image_bytes)
    print("识别结果：", res_ocr)
    res = text_utils.match_listened_minutes(res_ocr)
    if res == -1:
        print("未识别到听新闻分钟数！")
        return "unknown", None
    print("已听", res, "分钟")
    # 将res转为数字，如果res >= 60,则打印听新闻完成，否则打印任务未完成
    if res >= 60:
        print("==[success]== ✅听新闻任务完成！")
        return "done", None
    else:
        # 计算剩余时间
        remain = 60 - res
        print("==[info]==📢听新闻任务正在进行中……")
        return "ing", remain
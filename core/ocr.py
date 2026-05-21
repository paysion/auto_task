import requests
import base64
import time
import utils.text_utils as text_utils
from config.settings import OCR_ACCOUNTS
import utils.image_utils as image_utils
import core.adb as adb

# 每个账号独立缓存 token：(api_key, secret_key) -> (token, expire)
_token_cache = {}
# 当前使用的账号索引，0 为默认
_current_account = 0

def _get_token(account_index):
    global _token_cache

    account = OCR_ACCOUNTS[account_index]
    cache_key = (account["api_key"], account["secret_key"])

    token, expire = _token_cache.get(cache_key, (None, 0))
    if token and time.time() < expire:
        return token

    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": account["api_key"],
        "client_secret": account["secret_key"],
    }

    res = requests.get(url, params=params).json()
    token = res["access_token"]
    _token_cache[cache_key] = (token, time.time() + res["expires_in"] - 60)
    return token

def _is_quota_exhausted(res):
    """每天请求限额用完"""
    return res.get("error_code") == 17

def _is_success(res):
    return "words_result" in res

def ocr_image(image_bytes):
    global _current_account

    img_b64 = base64.b64encode(image_bytes)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"image": img_b64}

    for offset in range(len(OCR_ACCOUNTS)):
        idx = (_current_account + offset) % len(OCR_ACCOUNTS)
        token = _get_token(idx)
        url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}"

        res = requests.post(url, data=data, headers=headers).json()
        # print("原始OCR结果：", res)

        if _is_success(res):
            _current_account = idx
            return text_utils.clean_ocr_text(res)

        if _is_quota_exhausted(res):
            print(f"账号 {idx} 今日额度用完，切换下一个")
            continue
        else:
            # 非额度错误（如识别失败），也尝试下一个账号
            print(f"账号 {idx} 识别失败: {res.get('error_msg', '未知错误')}，切换下一个")
            continue

    print("==[error]== 所有OCR账号均不可用")
    return ""

# 识别听新闻的分钟数
def ocr_minutes():
    """
    unknown表示未识别，done表示已完成，ing表示正在进行
    """
    image = adb.screencap()
    image_bytes = image_utils.encode_png(image)
    res_ocr = ocr_image(image_bytes)
    # print("识别结果：", res_ocr)
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

# 识别是否在看视频界面，匹配“评论” “分享”两个词语
def ocr_watching_video():
    image = adb.screencap()
    image_bytes = image_utils.encode_png(image)
    res_ocr = ocr_image(image_bytes)
    # print("识别结果：", res_ocr)
    if "评论" in res_ocr and "分享" in res_ocr:
        return True
    else:
        return False

# 识别弹出的未登录弹窗
def ocr_unlogin_popup():
    image = adb.screencap()
    image_bytes = image_utils.encode_png(image)
    res_ocr = ocr_image(image_bytes)
    print("识别结果：", res_ocr)
    # 匹配是否有“登录后才可获得任务积分奖励”
    if "登录后才可获得任务积分奖励" in res_ocr:
        return True
    else:
        return False
    

if __name__ == "__main__":
    ocr_minutes()
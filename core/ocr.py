import requests
import base64
import time
from utils.text_clean import clean_ocr_text
from config.settings import API_KEY, SECRET_KEY

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
    return clean_ocr_text(res)

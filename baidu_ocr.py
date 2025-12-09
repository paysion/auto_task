import requests
import base64
import re

# 1. 获取 token（如果你已有 token，这部分可跳过）
API_KEY = "Wnl3lfYyjcdQyh8I8PRF4qYx"
SECRET_KEY = "HXZFSYEs7D6w4lwC4v3kO0lEI2b0CH2A"

token_url = "https://aip.baidubce.com/oauth/2.0/token"
token_params = {
    "grant_type": "client_credentials",
    "client_id": API_KEY,
    "client_secret": SECRET_KEY
}
token_res = requests.get(token_url, params=token_params).json()
access_token = token_res["access_token"]

# 2. 读取图像并进行 OCR
ocr_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}"
# 读取templates/screenshots目录下的图片
with open("templates/screenshots/watch_news_202512081011.png", "rb") as f:
    img = base64.b64encode(f.read())

data = {"image": img}
headers = {"content-type": "application/x-www-form-urlencoded"}

ocr_res = requests.post(ocr_url, data=data, headers=headers).json()
lines = []
for item in ocr_res["words_result"]:
    txt = item["words"].strip()
    
    # 去除单个符号或无意义噪声
    if len(txt) <= 2 and re.match(r'^[^\u4e00-\u9fa5a-zA-Z0-9]+$', txt):
        continue

    lines.append(txt)

# 合并文本（保留自然段）
text = ""
for i, line in enumerate(lines):
    if text and not text.endswith(("。", "！", "？")):
        text += line
    else:
        text += ("\n" if i > 0 else "") + line

print(text)


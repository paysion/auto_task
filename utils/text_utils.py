import re

# 清洗ocr识别的结果
def clean_ocr_text(ocr_json):
    if "words_result" not in ocr_json:
        return ""

    lines = []
    for item in ocr_json["words_result"]:
        t = item["words"].strip()
        if len(t) <= 2 and re.match(r'^[^\u4e00-\u9fa5a-zA-Z0-9]+$', t):
            continue
        lines.append(t)

    text = ""
    for i, line in enumerate(lines):
        if text and not text.endswith(("。", "！", "？")):
            text += line
        else:
            text += ("\n" if i > 0 else "") + line
    print(text)
    return text.strip()

# 匹配文中中的“已听xx分钟”，eg:火灾高市已听82分钟下跌突袭
def match_listened_minutes(text):
    match = re.search(r'已听(\d+)分钟', text)
    if match:
        return int(match.group(1))
    return 0

# 检查url是否是https://dj.jxnews.com.cn/开头的
def check_url(url):
    return url.startswith("https://dj.jxnews.com.cn/")

import re

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

    return text.strip()

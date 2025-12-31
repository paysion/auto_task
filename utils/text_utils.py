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
    return -1

# 从文本中提取话题
def extract_topics(text: str):
    """
    从文本中提取话题列表（不包含序号）
    """
    topics = []
    i = 0
    n = len(text)
    
    while i < n:
        # 如果当前位置是单个数字序号（1-9）
        if text[i].isdigit() and (i == 0 or not text[i-1].isdigit()):
            seq = text[i]  # 序号
            start = i + 1  # 内容起始位置
            i += 1
            # 找下一个单个数字序号的位置
            while i < n:
                if text[i].isdigit() and (i+1 >= n or not text[i+1].isdigit()):
                    break
                i += 1
            content = text[start:i].strip()
            if content:
                topics.append(content)
        else:
            i += 1
    return topics


def clean_topic(topic):
    # "关键字搜索搜索"前面的文本全部删除,包括"搜索"
    topic = re.sub(r'^.*?关键字搜索搜索', '', topic)

    # 规则2：删除“数字+阅读” 和 “数字+参与”
    topic = re.sub(r'选择\d+阅读', '', topic)
    topic = re.sub(r'\d+参与', '', topic)

    # 可选：压缩多余空白
    topic = re.sub(r'\s+', ' ', topic).strip()

    return topic.strip()


def extract_topics_from_ocr(ocr_text):
    """
    从OCR识别文本中提取话题
    
    参数:
    ocr_text: OCR识别出的原始文本
    
    返回:
    list: 清洗后的话题列表
    """
    topics = []
    
    # 按行分割文本
    lines = ocr_text.strip().split('\n')
    
    for line in lines:
        # 跳过空行
        if not line.strip():
            continue
            
        # 使用正则表达式匹配数字开头的话题行
        # 格式如: "1话题内容选择1234阅读456参与"
        # 或者: "10话题内容选择1234阅读456参与"
        
        # 匹配数字+点或数字+空格开头，然后是任意字符，直到遇到"选择"
        pattern1 = r'^\d+[\.、]?\s*(.+?)\s*选择\d+'
        # 匹配直接以话题内容开头的行（可能是无编号的）
        pattern2 = r'^(.+?)\s*选择\d+'
        
        match = re.search(pattern1, line)
        if not match:
            match = re.search(pattern2, line)
            
        if match:
            topic = match.group(1).strip()
            # 清理可能的多余空格和特殊字符
            topic = re.sub(r'\s+', ' ', topic)
            topics.append(topic)
    
    return topics

# 检查url是否是https://dj.jxnews.com.cn/开头的
def check_url(url):
    return url.startswith("https://dj.jxnews.com.cn/")

from openai import OpenAI
import os
import random
from config.settings import DEEPSEEK_API_KEY


styles = ["自然", "严谨", "幽默", "深刻"]

def gen_comment(text):
    """
    根据新闻内容 / 视频标题生成评论
    """
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com")
    word_count = random.randint(15, 40)
    chosen_style = random.choice(styles)
    prompt = f"""
        请根据下面内容生成一条短评:
        {text}
        
        要求:
        1.内容积极向上，不要出现政治内容
        2.字数随机{word_count}字
        3.风格{chosen_style}
        """
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个人民日报的新闻读者"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content
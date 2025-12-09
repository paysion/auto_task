from openai import OpenAI
import os


def gen_comment(text):
    """
    根据新闻内容 / 视频标题生成评论
    """
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

    prompt = f"请根据下面内容生成一条简短自然的评论，要求内容积极向上，不要出现政治内容，20字左右：\n{text}"
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个新闻读者"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content
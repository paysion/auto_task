from openai import OpenAI
import random
from config.settings import DEEPSEEK_API_KEY, CHATAPI_US_API_KEY


styles = ["自然", "严谨", "幽默", "深刻"]

def _build_prompt(text):
    """
    构造统一 Prompt
    """
    word_count = random.randint(15, 40)
    style = random.choice(styles)
    return f"""
            请根据下面内容生成一条短评:
            {text}

            要求:
            1. 内容积极向上，不要出现政治内容
            2. 字数约 {word_count} 字
            3. 风格：{style}
            """

def gen_comment(text):
    """
    根据新闻内容 / 视频标题生成评论
    """
    # 基本验证
    if not text or not isinstance(text, str) or text.strip() == "":
        return "unknown"
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com")

    prompt = _build_prompt(text)
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位理性、正面的新闻读者"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    if response.choices[0] is None:
        return "unknown"
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def gen_comment_gptapi(text):
    """
    使用 gptapi.us 中转的 DeepSeek 模型
    """
    client = OpenAI(
        api_key=CHATAPI_US_API_KEY,
        base_url="https://api.gptapi.us/v1/chat/completions"
    )

    prompt = _build_prompt(text)

    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False
    )
    print(response,"\n")
    return response.choices[0].message.content

if __name__ == "__main__":
    demo_text = "国产新能源车销量持续增长，技术创新推动行业升级。"

    # print("=== DeepSeek 官方 ===")
    # print(gen_comment(demo_text))

    print("\n=== gptapi.us 中转 ===")
    print(gen_comment_gptapi(demo_text))
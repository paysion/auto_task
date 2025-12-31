import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import core.ocr as ocr
import core.adb as adb
import utils.image_utils as image_utils
import utils.text_utils as text_utils
import cv2

def chrome_open(url):
    opts = Options()
    #opts.add_argument("--headless")  # 无头模式，不弹窗
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    time.sleep(3)  # 加载页面，确保计入分享
    driver.quit()

def task_share_news():
    url = "https://dj.jxnews.com.cn/webDetails/news?id=12893484&tenantId=312&uid=68f6e331fd9bbf0019b337db"
    chrome_open(url)
    print("分享任务完成！")

# 识别听新闻的分钟数
def ocr_minutes():
    image = adb.screencap()
    image_bytes = image_utils.encode_png(image)
    res_ocr = ocr.ocr_image(image_bytes)
    print("识别结果：", res_ocr)
    res = text_utils.match_listened_minutes(res_ocr)
    print("已听", res, "分钟")
    # 将res转为数字，如果res > 60,则打印听新闻完成，否则打印任务未完成
    if res > 60:
        print("听新闻任务完成！")
    else:
        print("听新闻任务未完成！")

# ocr识别话题    
def ocr_topic():
    image = adb.screencap()
    #image_path = "templates/screenshots/topic.png"
    # 从路径中读取图片
    #image = cv2.imread(image_path)
    # if image is None:
    #     raise FileNotFoundError(f"图片读取失败: {image_path}")
    image_bytes = image_utils.encode_png(image)
    res_ocr = ocr.ocr_image(image_bytes)
    print("\n识别结果：", res_ocr)
    topics_clean = text_utils.clean_topic(res_ocr)
    print("\n第一遍清洗：", topics_clean)
    topics = text_utils.extract_topics(topics_clean)
    print("\n话题：", topics)



if __name__ == "__main__":
    task_share_news()
    #ocr_minutes()
    #ocr_topic()

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def chrome_open(url):
    opts = Options()
    opts.add_argument("--headless")  # 无头模式，不弹窗
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

if __name__ == "__main__":
    task_share_news()

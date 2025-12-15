import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_chrome_driver():
    opts = Options()
    opts.add_argument("--headless")      # 无头模式
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)
    return driver

def chrome_open(driver, url):
    # 使用同一个 driver 打开不同链接
    driver.get(url)
    time.sleep(3)  # 给页面加载时间

def share_news(url):
    chrome_open(url)
    print("分享任务完成！")

def __init__():
    #task_share_news()
    print("初始化完成！")
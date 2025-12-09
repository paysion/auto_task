import schedule
import time
from tasks.task_news import watch_news

def run_daily():
    schedule.every().day.at("09:00").do(watch_news)

    while True:
        schedule.run_pending()
        time.sleep(1)

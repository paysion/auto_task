import schedule
import time
import tasks.task as task

def run_daily():
    schedule.every().day.at("09:00").do(task.run_tasks)

    while True:
        schedule.run_pending()
        time.sleep(1)

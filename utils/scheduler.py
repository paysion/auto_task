import schedule
import time
import tasks.task as task
import config.accounts as accounts
import utils.account_switcher as account_switcher

def run_all_accounts():
    """
    执行所有账号的任务
    """
    print(">>> [Scheduler] 开始执行所有账号任务 <<<")

    for _ in range(len(accounts.ACCOUNTS)):
        task.run_tasks()
        account_switcher.switch_to_next_account()

    print(">>> [Scheduler] 所有账号任务执行完毕 <<<\n")

def run_daily():
    """
    每日定时任务：每天 02:00 执行一次 run_all_accounts
    """
    schedule.every().day.at("02:00").do(run_all_accounts)

    print(">>> 每日计划任务已启动，等待执行 <<<")
    while True:
        schedule.run_pending()
        time.sleep(1)

import tasks.task as task
import utils.account_switcher as account_switcher
import config.accounts as accounts
from utils.scheduler import run_daily
import time

if __name__ == "__main__":
    print(">>> 自动化任务系统启动 <<<")

    # 循环账号ACCOUNTS的长度
    for _ in range(len(accounts.ACCOUNTS)):
        task.run_tasks()
        account_switcher.switch_to_next_account()

    # 立即执行一次
    #task.run_tasks()

    # 开启每日调度
    # run_daily()

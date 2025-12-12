import tasks.task as task
import utils.account_switcher as account_switcher
import config.accounts as accounts
from utils.scheduler import run_daily
import utils.scheduler as scheduler

if __name__ == "__main__":
    print(">>> 自动化任务系统启动 <<<")

    #task.run_tasks()
    # 循环账号ACCOUNTS的长度
    # for _ in range(len(accounts.ACCOUNTS)):
    #     task.run_tasks()
    #     account_switcher.switch_to_next_account()

    # 启动时先执行一次所有账号
    scheduler.run_all_accounts()

    # 开启每日调度（每天 09:00 执行）
    scheduler.run_daily()

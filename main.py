import tasks.task as task
from utils.scheduler import run_daily

if __name__ == "__main__":
    print(">>> 自动化任务系统启动 <<<")

    # 立即执行一次
    task.run_tasks()

    # 开启每日调度
    # run_daily()

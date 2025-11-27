import time
from vision import find_template, find_text
from control import click, scroll_down


# ----------------------------------------------------------
# 自动点击模板按钮
# ----------------------------------------------------------
def click_template(path, name="", retry=5):
    """
    点击模板按钮
    path: 模板图片路径
    name: 按钮名称
    retry: 重试次数
    """

    for _ in range(retry):
        pos = find_template(path)
        if pos:
            print(f"[点击按钮] {name}")
            click(*pos)
            time.sleep(1)
            return True
    print(f"[未找到按钮] {name}")
    return False


# ----------------------------------------------------------
# 自动点击文字按钮（例如 “未完成”）
# ----------------------------------------------------------
def click_text(keywords, name="", retry=5):
    for _ in range(retry):
        pos = find_text(keywords)
        if pos:
            print(f"[点击文字] {name}")
            click(*pos)
            time.sleep(1)
            return True
    print(f"[未找到文字] {name}")
    return False


# ----------------------------------------------------------
# 视频任务执行逻辑（观看 10 条视频，每条 30s）
# ----------------------------------------------------------
def do_video_task(times=10, wait_seconds=30):
    print("\n=== 开始执行【看视频】任务 ===")

    # 点击“热点”进入视频流
    click_template("templates/video_hot_btn.png", "热点按钮")

    for i in range(times):
        print(f"\n▶ 开始观看第 {i+1}/{times} 条视频")
        time.sleep(wait_seconds)

        # 下滑，下一个视频
        scroll_down(800)

    print("\n=== 视频任务完成 ===")

    # 返回积分任务页面（你可以手动按一下返回键）
    time.sleep(1)

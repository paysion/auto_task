from adb_wrapper import tap, swipe, screenshot
from vision import match_template, find_text
import time


def click_by_template(path, name="", timeout=5):
    for _ in range(timeout):
        img = screenshot()
        pos = match_template(img, path)
        if pos:
            print(f"[OK] 找到 {name} 点击位置: {pos}")
            tap(*pos)
            time.sleep(1)
            return True
        time.sleep(1)
    print(f"[FAIL] 没找到 {name}")
    return False


def click_by_text(words, name="", timeout=5):
    for _ in range(timeout):
        img = screenshot()
        pos = find_text(img, words)
        if pos:
            print(f"[OK] 识别到文字 {name}, 点击: {pos}")
            tap(*pos)
            time.sleep(1)
            return True
        time.sleep(1)
    return False


# =======================================
#       视频任务示例（循环播放）
# =======================================
def do_watch_video(count=10):
    for i in range(count):
        print(f"\n==== 开始第 {i+1} 个视频 ====")

        # 点击进入视频（模板匹配）
        click_by_template("templates/btn_watch.png", "进入视频")

        # 等 30 秒（你可改成 OCR 检测 "视频完成"）
        time.sleep(30)

        # 滑动到下一个视频
        swipe(500, 1500, 500, 500, 300)
        time.sleep(1)

    print("\n===== 视频任务完成！=====")

import core.adb as adb

# ---------------- 测试 ----------------
if __name__ == "__main__":
    print("剪贴板内容:", adb.get_clipboard())
    # 示例点击
    # tap(500, 500)
    # 示例滑动
    # human_swipe()
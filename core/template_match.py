import cv2
import os
def find_template(screen, template_path, threshold=0.8):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")
    
    tpl = cv2.imread(template_path)
    if tpl is None:
        raise ValueError(f"无法加载模板图片: {template_path}")
    
    h, w = tpl.shape[:2]
    # 截图与模板都转换为灰度
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    
    # 使用TM_CCOEFF_NORMED
    result = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
    if result is None:
        return None,None, None
    
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    print(f"匹配度: {max_val:.4f}")
    
    if max_val < threshold:
        return None, None, None
    
    x = max_loc[0] + w // 2
    y = max_loc[1] + h // 2
    return x, y, max_val


def find_template_edge(screen, template_path, threshold=0.5):
    """
    基于边缘的模板匹配（背景颜色随意变化也能匹配稳定）
    
    参数:
        screen        - 截图 (BGR格式的numpy数组)
        template_path - 模板路径
        threshold     - 匹配阈值（值越大越严格，0.4~0.6常用）
        
    返回:
        (x, y, score) 或 (None, None, None)
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")

    tpl = cv2.imread(template_path)
    if tpl is None:
        raise ValueError(f"无法加载模板图片: {template_path}")

    h, w = tpl.shape[:2]

    # ---- 灰度化 ----
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)

    # ---- Canny提取边缘（重点）----
    screen_edge = cv2.Canny(screen_gray, 50, 150)
    tpl_edge = cv2.Canny(tpl_gray, 50, 150)

    # ---- 模板匹配 ----
    result = cv2.matchTemplate(screen_edge, tpl_edge, cv2.TM_CCOEFF_NORMED)
    if result is None:
        return None, None, None

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f"[Edge匹配] 匹配度: {max_val:.4f}")

    if max_val < threshold:
        return None, None, None

    # 中心坐标
    x = max_loc[0] + w // 2
    y = max_loc[1] + h // 2
    return x, y, max_val


def find_template_hu(screen, template_path, threshold=0.3):
    """
    使用 Hu 矩（形状匹配）来定位模板位置。
    优点：不在意颜色、亮度、背景，只看轮廓形状。
    
    参数：
        screen        - 截图（BGR numpy array）
        template_path - 模板路径
        threshold     - 形状匹配阈值（值越小越相似，0.1~0.5 之间常用）
    
    返回：
        (x, y, score) 或 (None, None, None)
    """
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")
    
    tpl = cv2.imread(template_path)
    if tpl is None:
        raise ValueError(f"无法加载模板图片: {template_path}")

    # ---- 灰度 + 二值化（用于提取轮廓） ----
    gray_tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    _, th_tpl = cv2.threshold(gray_tpl, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, th_screen = cv2.threshold(gray_screen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ---- 找模板的主轮廓 ----
    contours_tpl, _ = cv2.findContours(th_tpl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_tpl) == 0:
        return None, None, None
    cnt_tpl = max(contours_tpl, key=cv2.contourArea)

    h, w = gray_tpl.shape[:2]

    best_score = 999
    best_loc = None

    # ---- 滑窗遍历屏幕（类似模板匹配，但只比较形状） ----
    for y in range(0, screen.shape[0] - h, max(2, h // 10)):
        for x in range(0, screen.shape[1] - w, max(2, w // 10)):

            roi = th_screen[y:y+h, x:x+w]

            contours_roi, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours_roi) == 0:
                continue

            cnt_roi = max(contours_roi, key=cv2.contourArea)

            # Hu 矩形状匹配（越小越相似）
            score = cv2.matchShapes(cnt_tpl, cnt_roi, cv2.CONTOURS_MATCH_I1, 0)

            if score < best_score:
                best_score = score
                best_loc = (x, y)

    # ---- 阈值判断 ----
    print(f"[Hu匹配] 形状相似度: {best_score:.4f}")

    if best_loc is None or best_score > threshold:
        return None, None, None

    x, y = best_loc
    center_x = x + w // 2
    center_y = y + h // 2

    return center_x, center_y, best_score



if __name__ == "__main__":
    # 尝试不同的路径
    screen = cv2.imread("../templates/screenshots/living_video.png")
    print(f"屏幕截图尺寸: {screen.shape}")
    
    # 尝试不同的模板路径
    template_path = "../templates/buttons/living_video_btn.png"
    
    # 添加debug=True参数
    result = find_template(screen, template_path, threshold=0.8)
    
    if result is None:
        print("模板未找到，可能原因:")
        print("1. 图片分辨率/缩放不同")
        print("2. 颜色/亮度不同")
        print("3. 模板不存在于屏幕中")
        print("4. 需要调整阈值")
        
        # 尝试多种匹配方法
        methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']
        
        tpl = cv2.imread(template_path)
        print(f"\n测试不同匹配方法:")
        for method_name in methods:
            method = eval(method_name)
            result = cv2.matchTemplate(screen, tpl, method)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            print(f"{method_name}: {max_val:.4f}")
    else:
        print(f"找到模板: {result}")


def find_best_template(screenshot, template_paths, min_score=0.0):
    """
    在多个模板中选择匹配度最高的一个

    :param screenshot: 当前截图（adb.screencap() 的返回值）
    :param template_paths: 模板图片路径列表
    :param matcher: 模板匹配函数（如 template_match.find_template）
    :param min_score: 最低可接受匹配度
    :return: (best_x, best_y, best_score, best_template_path) 或 (None, None, None, None)
    """
    best_result = (None, None, None, None)
    best_score = min_score

    for path in template_paths:
        x, y, score = find_template(screenshot, path)

        # 未匹配到直接跳过
        if x is None or y is None or score is None:
            continue

        # 选择匹配度更高的
        if score > best_score:
            best_score = score
            best_result = (x, y, score, path)

    return best_result

def find_button(desc, screenshot, template_paths, min_score=0.6):
    """
    查找匹配度最高的按钮，找不到直接失败

    :return: (x, y) 或 None
    """
    x, y, score, path = find_best_template(
        screenshot, template_paths, min_score=min_score
    )

    if x is None:
        print(f"==[error]==❌ 未找到【{desc}】按钮")
        return None

    print(f"==[info]==📢匹配度最高的【{desc}】按钮：{path}，score={score:.2f}")
    return x, y


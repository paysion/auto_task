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

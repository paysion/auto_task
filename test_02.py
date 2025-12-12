import core.ocr as ocr
import core.adb as adb
import core.template_match as template_match
import cv2


if __name__ == "__main__":
    
    screen = adb.screencap()
    # 匹配直播回顾按钮
    template_path = "./templates/buttons/live_video_btn.png"
    result = template_match.find_template(screen, template_path)
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

    # 编码为 PNG 二进制
    # _, encoded_img = cv2.imencode(".png", img)
    # image_bytes = encoded_img.tobytes()

    # ocr.ocr_image(image_bytes)
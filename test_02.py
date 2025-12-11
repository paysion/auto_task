import core.ocr as ocr
import core.adb as adb
import core.template_match as template_match
import cv2


if __name__ == "__main__":
    
    img = adb.screencap()
    # 匹配直播回顾按钮
    template_path = "./templates/buttons/live_video_btn.png"
    x, y, _ = template_match.find_template(img, template_path)
    # x,y不为空则点击
    if x and y:
        adb.tap(x, y)

    # 编码为 PNG 二进制
    # _, encoded_img = cv2.imencode(".png", img)
    # image_bytes = encoded_img.tobytes()

    # ocr.ocr_image(image_bytes)
import core.ocr as ocr
import core.adb as adb
import cv2

if __name__ == "__main__":
    
    img = adb.screencap()
    # 编码为 PNG 二进制
    _, encoded_img = cv2.imencode(".png", img)
    image_bytes = encoded_img.tobytes()

    ocr.ocr_image(image_bytes)
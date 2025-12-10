import cv2

# 编码为 PNG 二进制
def encode_png(img):
    _, encoded_img = cv2.imencode(".png", img)
    return encoded_img.tobytes()
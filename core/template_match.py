import cv2

def find_template(screen, template_path, threshold=0.8):
    tpl = cv2.imread(template_path)
    h, w = tpl.shape[:2]

    result = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    x = max_loc[0] + w // 2
    y = max_loc[1] + h // 2
    return x, y, max_val

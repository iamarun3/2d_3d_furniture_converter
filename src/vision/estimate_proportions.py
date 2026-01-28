import cv2

def estimate(image_path, box):
    """
    box = [x1, y1, x2, y2]
    """

    img = cv2.imread(image_path)
    h, w, _ = img.shape

    x1, y1, x2, y2 = box

    chair_width = x2 - x1
    chair_height = y2 - y1

    width_ratio = chair_width / w
    height_ratio = chair_height / h

    print("📐 Width ratio:", round(width_ratio, 2))
    print("📐 Height ratio:", round(height_ratio, 2))

    # Convert ratios to 3D chair parameters (heuristics)
    params = {
        "seat_width": 0.4 + width_ratio,          # base + ratio
        "seat_depth": 0.4 + width_ratio * 0.5,
        "leg_height": 0.3 + height_ratio * 0.4,
        "back_height": 0.4 + height_ratio * 0.6,
        "color": (0.6, 0.3, 0.1, 1)   # wooden color
    }

    print("🪑 Estimated 3D params:", params)

    return params

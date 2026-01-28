from vision.detect_furniture import detect
from vision.estimate_proportions import estimate

image_path = "data/test.jpg"

result = detect(image_path)

if result:
    params = estimate(image_path, result["box"])
    print("Final params to send to Blender:", params)
else:
    print("⚠️ Using fallback default parameters")

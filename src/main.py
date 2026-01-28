from vision import detect_furniture, detect_parts, estimate_proportions
from reconstruction import confidence_check, fallback
from blender import chair_template

image_path = "../data/test.jpg"

# Step 1: Detect furniture
furniture = detect_furniture.detect(image_path)

# Step 2: Confidence check
if confidence_check.is_confident(furniture["confidence"]):
    parts = detect_parts.detect(image_path)
    params = estimate_proportions.estimate(parts)
else:
    params = fallback.get_default()

# Step 3: Generate 3D
chair_template.create_chair(params)

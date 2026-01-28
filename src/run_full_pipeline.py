import subprocess
from vision.detect_furniture import detect
from vision.estimate_proportions import estimate

image_path = "data/test.jpg"

# Step 1 – Detect
result = detect(image_path)

if not result:
    print("❌ No chair detected, stopping.")
    exit()

# Step 2 – Estimate proportions
params = estimate(image_path, result["box"])

# Step 3 – Call Blender with params
blender_path = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
# ⚠️ CHANGE THIS PATH if your Blender is in different location

cmd = [
    blender_path,
    "--background",
    "--python", "src/blender/chair_template.py",
    "--",
    "--seat_width", str(params["seat_width"]),
    "--seat_depth", str(params["seat_depth"]),
    "--leg_height", str(params["leg_height"]),
    "--back_height", str(params["back_height"])
]

print("🚀 Launching Blender to generate 3D model...")
subprocess.run(cmd)

print("🎉 Pipeline finished! Check Desktop for ai_generated_chair.glb")

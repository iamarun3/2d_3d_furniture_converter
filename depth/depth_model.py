import torch
import cv2
import numpy as np
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python depth_model.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

if not os.path.isfile(image_path):
    print("Image not found:", image_path)
    sys.exit(1)

device = torch.device("cpu")

model_type = "DPT_Large"

midas = torch.hub.load("intel-isl/MiDaS", model_type, trust_repo=True)
midas.to(device)
midas.eval()

midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
transform = midas_transforms.dpt_transform

img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

input_batch = transform(img).to(device)

with torch.no_grad():
    prediction = midas(input_batch)

prediction = torch.nn.functional.interpolate(
    prediction.unsqueeze(1),
    size=img.shape[:2],
    mode="bicubic",
    align_corners=False,
).squeeze()

depth_map = prediction.cpu().numpy()
depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
depth_map = (depth_map * 255).astype(np.uint8)

output_dir = os.path.join(os.getcwd(), "data", "output")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "depth.png")
cv2.imwrite(output_path, depth_map)

print("Depth map saved successfully at:", output_path)

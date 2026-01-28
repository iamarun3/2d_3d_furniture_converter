import os
import cv2
import numpy as np

print("Working directory:", os.getcwd())

output_dir = os.path.join(os.getcwd(), "data", "output")
os.makedirs(output_dir, exist_ok=True)

img = np.zeros((200, 200), dtype=np.uint8)
img[50:150, 50:150] = 255

output_path = os.path.join(output_dir, "test.png")
success = cv2.imwrite(output_path, img)

print("Saved to:", output_path)
print("Save success:", success)

from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def detect(image_path):
    print("🔍 Detecting furniture...")

    results = model(image_path)
    img = cv2.imread(image_path)

    best = None
    best_conf = 0.0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = model.names[cls]
            conf = float(box.conf[0])

            print(f"Detected: {name} with confidence {conf:.2f}")

            if name == "chair" and conf > best_conf:
                best_conf = conf
                best = {
                    "type": "chair",
                    "confidence": conf,
                    "box": box.xyxy[0].tolist()
                }

    if best:
        x1, y1, x2, y2 = map(int, best["box"])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"Chair {best['confidence']:.2f}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.imwrite("outputs/detected_chair.jpg", img)
        print("✅ Best chair detected with confidence:", best["confidence"])
        return best

    else:
        print("❌ No chair detected at all")
        return None

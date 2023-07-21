import ultralytics

ultralytics.checks()
from ultralytics import YOLO

import os

def classify_yolo(hash):
    model = YOLO("yolo/model.pt")
    model = YOLO("yolo/weights.pt")
    data_path = f"uploads/{hash}/inputs/"

    outputs = []

    for i in os.listdir(data_path):
        predictions = model.predict(source=data_path + i, save=True)
        for result in predictions:
            b = result.names
        for i in range(len(result.boxes)):
            box = result.boxes[i]
            cords = box.xyxy[0].tolist()
            class_id = box.cls[0].item()
            if (
                b[class_id] == "button"
                or b[class_id] == "image"
                or b[class_id] == "link"
                or b[class_id] == "text"
            ):
                outputs.append({
                    'type': b[class_id],
                    'coordinates': cords
                })
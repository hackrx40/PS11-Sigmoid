# -*- coding: utf-8 -*-
"""entity_extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lzDEpFXlmcFICF3m6WCm2UUok0YtK4Z0
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install ultralytics
import ultralytics
ultralytics.checks()
from ultralytics import YOLO
from PIL import Image, ImageDraw

from google.colab import drive
drive.mount('/content/drive')

import cv2,os
model = YOLO('/content/drive/MyDrive/Website Screenshots Dataset MIT/yolov8m.pt')
model = YOLO('/content/drive/MyDrive/Website Screenshots Dataset MIT/best (3).pt')
data_path = "/content/drive/MyDrive/Website Screenshots Dataset MIT/Personal Loan PDP/"
for i in os.listdir(data_path):
    predictions=model.predict(source=data_path+i,save=True)
    #display(Image.open('runs/detect/predict33/cropped_2 (1).png'))#original predictions
    for result in predictions:
      a=result.boxes.xyxy #Tensor coordinates-all images
      b=result.names #class annot
    print("num classes predicted", len(result.boxes))
    image = Image.open(data_path+i)
    draw = ImageDraw.Draw(image)
    for i in range(len(result.boxes)):
      box = result.boxes[i]
      cords = box.xyxy[0].tolist()
      class_id = box.cls[0].item()
      conf = box.conf[0].item()
      if b[class_id]=="button" or b[class_id]=="image" or b[class_id]=="link" or b[class_id]=="text":
          print("Object type:", class_id)
          print("Class :", b[class_id])
          print("Coordinates:", cords)
          x_min, y_min, x_max, y_max = cords
          x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
          entity = image.crop((x_min, y_min, x_max, y_max))
          entity.save(f'entity_{i}.png')
          entity.show()
          draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
    image.show()
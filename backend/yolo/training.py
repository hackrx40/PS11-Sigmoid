# -*- coding: utf-8 -*-
"""YOLOV8m 25 .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r9hrQxNzeY8MvX09huzkNBDF-uK4mQ2H
"""

pip install roboflow

import os
HOME = os.getcwd()
print(HOME)

!pip install ultralytics

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

from ultralytics import YOLO

# Commented out IPython magic to ensure Python compatibility.
!mkdir {HOME}/datasets
# %cd {HOME}/datasets

!pip install roboflow --quiet

from roboflow import Roboflow
rf = Roboflow(api_key="lQnzCQs4mhnBTHAJGbly")
project = rf.workspace("roboflow-gw7yv").project("website-screenshots")
dataset = project.version(1).download("yolov8")

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=train model=yolov8m.pt data={dataset.location}/data.yaml epochs=25 imgsz=800 plots=True

# Commented out IPython magic to ensure Python compatibility.
from IPython.display import display, Image
# %cd {HOME}
!yolo task=detect mode=val model={HOME}/runs/detect/train2/weights/best.pt data={dataset.location}/data.yaml

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train2/weights/best.pt conf=0.25 source={dataset.location}/addons_mozilla_org_png.rf.8pWFwr9ZblJ92BQghXBW (1).jpg save=True

!yolo export model=yolov8n.pt format=tflite

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train2/weights/best.pt conf=0.25 source={dataset.location}/test/images save=True

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train2/weights/best.pt conf=0.25 source={HOME}/aums.PNG save=True

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train2/weights/best.pt conf=0.25 source={HOME}/screenshot_14.png save=True

!yolo export model=yolov8m.pt format=tflite
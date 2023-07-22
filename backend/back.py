import os
import hashlib
from flask import Flask, request
import cv2
import numpy as np
from keras.models import load_model
import time
import json
from flask_cors import CORS

from screenshot import take_screenshot
from comparison import get_contours_diff
from yolo.entity_extraction import classify_yolo

app = Flask(__name__)
CORS(app)


def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        img = cv2.imread(os.path.join(folder_path, filename))
        if img is not None:
            external_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

            # Resize the image to match the input size of the model
            target_size = (240, 518)
            external_image = cv2.resize(external_image, target_size)
            external_image = external_image.astype('float32') / 255.0

            images.append(external_image)
    return images


def load_dataset(dataset_path):
    images = load_images_from_folder(dataset_path)
    labels = [0] * len(images)
    return np.array(images), np.array(labels)


def calculate_iou(box1, box2):
    # Calculate the coordinates of the intersection rectangle
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # Check for non-overlapping rectangles
    if x2 < x1 or y2 < y1:
        return 0.0

    # Calculate the area of the intersection rectangle
    intersection_area = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Calculate the areas of both bounding boxes
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # Calculate the Union area by adding the areas of both bounding boxes and subtracting the intersection area
    union_area = box1_area + box2_area - intersection_area

    # Calculate the IoU
    iou = intersection_area / union_area

    return iou


@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        # Get the URL from the request
        url = request.form.get('url')

        if url is None:
            return "URL is missing in the request.", 400

        md5_hash = hashlib.md5((url + str(time.time())).encode()).hexdigest()
        folder_path = os.path.join('uploads', md5_hash)
        inputs_folder = os.path.join(folder_path, 'inputs')
        os.makedirs(inputs_folder, exist_ok=True)

        # Check if feature images are present
        if 'feature_images' in request.files:
            feature_images = request.files.getlist('feature_images')

            # Create the folder structure
            features_folder = os.path.join(folder_path, 'features')
            os.makedirs(features_folder, exist_ok=True)

            # Save feature images
            for image in feature_images:
                image_path = os.path.join(features_folder, image.filename)
                image.save(image_path)
            
        # Run the screenshot.py script for each size
        sizes = [ {'width': 375, 'height': 810, 'device_type': 'mobile'} ]

        for size in sizes:
            take_screenshot(url, size['width'], size['height'], md5_hash, size['device_type'])

        return {
            'hash': md5_hash,
            'images': os.listdir(inputs_folder)
        }

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/api/train', methods=['POST'])
def train():
    try:
        # Get the md5 hash from the request
        md5_hash = request.form.get('hash')

        if md5_hash is None:
            return "MD5 hash is missing in the request.", 400

        return "Skipped"

        # Load the feature images from the "features" subdirectory
        folder_path = os.path.join('uploads', md5_hash, 'features')
        images, labels = load_dataset(folder_path)

        # Load the saved model (dummy.h5)
        model_path = os.path.join('classify', 'dummy.h5')
        model = load_model(model_path)

        model.fit(images, labels)

        # Save the trained model inside the md5 folder
        trained_model_path = os.path.join('uploads', md5_hash, 'trained_model.h5')
        model.save(trained_model_path)

        return f"Model trained and saved successfully in the folder {md5_hash}."

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/api/generate_score', methods=['POST'])
def generate_score():
    hash = request.form.get('hash')

    # call the contour thing - inputs vs figma
    contours_diff, regions = get_contours_diff(hash)

    filters = json.loads(request.form.get('filters'))
    if any(filters.values()):
        excludes = []
        yolo_regions = classify_yolo(hash)
        for file in regions:
            local_excludes = []
            for i, contour in enumerate(file):
                highest_iou = 0
                for region in yolo_regions:
                    if region['type'] in filters and filters[region['type']]:
                        cords = region['coordinates']
                        highest_iou = max(calculate_iou(contour, cords), highest_iou)

                if highest_iou > 0.2:
                    local_excludes.append(contour)

            excludes.append(local_excludes)

        contours_diff, _ = get_contours_diff(hash, excludes)

    model_path = os.path.join('uploads', hash, 'trained_model.h5') if os.path.exists(os.path.join('uploads', hash, 'trained_model.h5')) else os.path.join('classify', 'classify.keras')
    model = load_model(model_path)
    model_3 = model.predict(np.array(load_images_from_folder(os.path.join('uploads', hash, 'inputs'))))

    return [model_3.flatten().tolist(), contours_diff]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

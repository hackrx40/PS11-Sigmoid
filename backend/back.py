import os
import hashlib
from flask import Flask, request
import cv2
import numpy as np
from keras.models import load_model
import time
from screenshot import take_screenshot
from comparison import get_contours_diff

app = Flask(__name__)


def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        img = cv2.imread(os.path.join(folder_path, filename))
        if img is not None:
            img = cv2.resize(img, (224, 224))  # Resize the images to a common size
            # img = cv2.resize(img, (375, 810)) # For newer model
            images.append(img)
    return images


def load_dataset(dataset_path):
    images = load_images_from_folder(dataset_path)
    labels = [1] * len(images)
    return np.array(images), np.array(labels)


@app.route('/upload', methods=['POST'])
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

        return md5_hash

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/train', methods=['POST'])
def train():
    try:
        # Get the md5 hash from the request
        md5_hash = request.form.get('hash')

        if md5_hash is None:
            return "MD5 hash is missing in the request.", 400

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


@app.route('/generate_score', methods=['POST'])
def generate_score():
    hash = request.form.get('hash')

    # call the contour thing - inputs vs figma
    contours_diff = get_contours_diff(hash)

    # if filters exist: any of button, text, image, link in filters is true
    # call yolo
    # filter yolo output with the filters
    # take IoU with respect to contour
    # get the percentage

    model = load_model(os.path.join('uploads', hash, 'trained_model.h5'))
    model_3 = model.predict(np.array(load_images_from_folder(os.path.join('uploads', hash, 'inputs'))))

    return [model_3.tolist(), contours_diff] #contour + yolo percentages


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

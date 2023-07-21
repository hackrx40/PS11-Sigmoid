import os
import hashlib
import subprocess
from flask import Flask, request
import cv2
import numpy as np
from keras.models import load_model
import time

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

        # Check if feature images are present
        if 'feature_images' in request.files:
            feature_images = request.files.getlist('feature_images')

            # Generate MD5 hash for folder name
            md5_hash = hashlib.md5(url.encode() + time.time()).hexdigest()

            # Create the folder structure
            folder_path = os.path.join('uploads', md5_hash)
            inputs_folder = os.path.join(folder_path, 'inputs')
            features_folder = os.path.join(folder_path, 'features')
            os.makedirs(inputs_folder, exist_ok=True)
            os.makedirs(features_folder, exist_ok=True)

            # Save feature images
            for image in feature_images:
                image_path = os.path.join(features_folder, image.filename)
                image.save(image_path)
        else:
            # Generate MD5 hash for folder name
            md5_hash = hashlib.md5(url.encode()).hexdigest()

            # Create the folder structure
            folder_path = os.path.join('uploads', md5_hash)
            inputs_folder = os.path.join(folder_path, 'inputs')
            os.makedirs(inputs_folder, exist_ok=True)

        # Run the screenshot.py script for each size
        script_path = 'screenshot.py'
        sizes = [
            {'width': 375, 'height': 810, 'device_type': 'Mobile'},
        ]

        for size in sizes:
            subprocess.call(['python', script_path, url, str(size['width']), str(size['height']), md5_hash, size['device_type']])

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

        # Train the model on the feature images
        # (You need to implement the training logic based on your model architecture and data)
        # For example: model.fit(images, labels, ...)
        model.fit(images, labels)

        # Save the trained model inside the md5 folder
        trained_model_path = os.path.join('uploads', md5_hash, 'trained_model.h5')
        model.save(trained_model_path)

        return f"Model trained and saved successfully in the folder {md5_hash}."

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/generate_score', methods=['POST'])
def generate_score():
    hash = request.form.hash

    model = load_model(os.path.join('uploads', hash, 'trained_model.h5'))
    return model(load_images_from_folder(os.path.join('uploads', hash, 'inputs')))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

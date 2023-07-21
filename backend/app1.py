import os
import hashlib
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get the URL from the request
        url = request.form.get('url')

        # Check if feature images are present
        if 'feature_images' in request.files:
            feature_images = request.files.getlist('feature_images')

            # Generate MD5 hash for folder name
            md5_hash = hashlib.md5(url.encode()).hexdigest()

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

        # Run the screenshot.py script
        script_path = 'screenshot.py'
        width = 390
        height = 844
        subprocess.call(['python', script_path, url, str(width), str(height)])

        # Move generated screenshots to inputs folder
        screenshots = os.listdir()
        for screenshot in screenshots:
            if screenshot.startswith('screenshot_'):
                screenshot_path = os.path.join(folder_path, 'inputs', screenshot)
                os.rename(screenshot, screenshot_path)

        return md5_hash

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run()

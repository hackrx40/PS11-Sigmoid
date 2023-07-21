import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_ssim(img1, img2):
    # Resize images to the same dimensions
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

    # Calculate the SSIM between the two images
    (score, _) = ssim(gray1, gray2, full=True)

    return score

def find_best_match(input_image, folder_path):
    best_score = -1
    best_match = None
    for filename in os.listdir(folder_path):
        img2 = cv2.imread(os.path.join(folder_path, filename))
        if img2 is not None:
            score = calculate_ssim(input_image, img2)
            if score > best_score:
                best_score = score
                best_match = img2

    return best_match, best_score

# Path to the folders containing images
folder1_path = 'backend/Images'
folder2_path = 'backend/test_image'
output_folder_path = 'backend/result'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Loop through images in the first folder
for filename in os.listdir(folder1_path):
    img1 = cv2.imread(os.path.join(folder1_path, filename))
    if img1 is not None:
        # Find the best match in the second folder
        best_match, best_score = find_best_match(img1, folder2_path)

        # Resize the best_match to the same height as img1
        best_match_resized = cv2.resize(best_match, (img1.shape[1], img1.shape[0]))

        # Create a subfolder corresponding to the current image from folder1_path
        subfolder_name = os.path.splitext(filename)[0]
        subfolder_path = os.path.join(output_folder_path, subfolder_name)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        # Save the best match image in the subfolder
        output_best_match_filename = f"best_match_{filename}"
        output_best_match_filepath = os.path.join(subfolder_path, output_best_match_filename)
        cv2.imwrite(output_best_match_filepath, best_match_resized)

        # Save the comparison image (concatenate img1 and best_match_resized side by side)
        comparison_image = np.concatenate((img1, best_match_resized), axis=1)
        
        # Convert images to grayscale for contour detection
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2_resized = cv2.cvtColor(best_match_resized, cv2.COLOR_BGR2GRAY)

        # Calculate and draw bounding box
        diff = cv2.absdiff(gray1, gray2_resized)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(comparison_image, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Save the comparison image with bounding boxes
        output_comparison_filename = f"comparison_{filename}"
        output_comparison_filepath = os.path.join(subfolder_path, output_comparison_filename)
        cv2.imwrite(output_comparison_filepath, comparison_image)

        # Write the similarity percentage to a file
        score_filename = f"similarity_percentage_{filename}.txt"
        score_filepath = os.path.join(subfolder_path, score_filename)
        with open(score_filepath, 'w') as f:
            f.write(f"Similarity Percentage: {best_score:.2f}\n")

# No need to display images

# Destroy any open windows
cv2.destroyAllWindows()

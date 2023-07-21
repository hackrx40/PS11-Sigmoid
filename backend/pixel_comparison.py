import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load the two images
img1 = cv2.imread('Spot-The-Differences/Images/camels1.jpg')
img2 = cv2.imread('Spot-The-Differences/Images/camels2.jpg')

# Resize images if necessary
img1 = cv2.resize(img1, (600, 360))
img2 = cv2.resize(img2, (600, 360))

# Convert images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Calculate the SSIM between the two images
(score, diff) = ssim(gray1, gray2, full=True)
diff = (diff * 255).astype("uint8")

# Apply threshold to obtain the differences
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Dilation
kernel = np.ones((5, 5), np.uint8)
dilate = cv2.dilate(thresh, kernel, iterations=2)

# Calculate contours
contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

total_pixels = gray1.shape[0] * gray1.shape[1]
difference_pixels = cv2.countNonZero(dilate)
similarity_percentage = (1 - (difference_pixels / total_pixels)) * 100
difference_percentage = (difference_pixels / total_pixels) * 100

for contour in contours:
    if cv2.contourArea(contour) > 100:
        # Calculate bounding box around contour
        x, y, w, h = cv2.boundingRect(contour)
        # Draw rectangle - bounding box on both images
        cv2.rectangle(img1, (x, y), (x+w, y+h), (0,0,255), 2)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0,0,255), 2)

        # Display similarity score on top of bounding box
        cv2.putText(img1, f"Score: {score:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(img2, f"Score: {score:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

# Show images with rectangles and similarity scores
x = np.zeros((img1.shape[0], 10, 3), np.uint8)
result = np.hstack((img1, x, img2))

# Print the total similarity percentage and difference percentage
print("Total Similarity Percentage:", similarity_percentage)
print("Total Difference Percentage:", difference_percentage)

# Display the images
cv2.imshow("Differences", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

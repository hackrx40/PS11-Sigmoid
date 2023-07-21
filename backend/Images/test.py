import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load the two images
img1 = cv2.imread('Spot-The-Differences/Images/sp3.png')
img2 = cv2.imread('Spot-The-Differences/Images/sp4.png')

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

# Calculate contours for Model 1
contours_model1 = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_model1 = imutils.grab_contours(contours_model1)

# Calculate contours for Model 2
contours_model2 = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_model2 = imutils.grab_contours(contours_model2)

# Calculate the IoU for each detected difference
iou_list = []
for contour_model1 in contours_model1:
    for contour_model2 in contours_model2:
        if len(contour_model1) == len(contour_model2):  # Check if contours have the same size
            intersection = cv2.contourArea(cv2.bitwise_and(contour_model1, contour_model2))
            area_model1 = cv2.contourArea(contour_model1)
            area_model2 = cv2.contourArea(contour_model2)
            union = area_model1 + area_model2 - intersection
            iou = intersection / union
            iou_list.append(iou)

# Calculate the average IoU
average_iou = np.mean(iou_list)
print("Average IoU:", average_iou)

# Draw rectangles on the images to indicate the differences
for contour_model1 in contours_model1:
    x, y, w, h = cv2.boundingRect(contour_model1)
    cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 0, 255), 2)

for contour_model2 in contours_model2:
    x, y, w, h = cv2.boundingRect(contour_model2)
    cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 0, 255), 2)

# Show images with rectangles on differences
x = np.zeros((img1.shape[0], 10, 3), np.uint8)
result = np.hstack((img1, x, img2))
cv2.imshow("Differences", result)

cv2.waitKey(0)
cv2.destroyAllWindows()

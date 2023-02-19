import cv2
import numpy as np
import imutils

# grayscale + blur로 사진 바꾸는 예제
image = cv2.imread("docs/raw_image/1cMBag.jpg")

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_gray_blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)

cv2.imshow("ImageShow", image_gray_blurred)
cv2.waitKey(0)

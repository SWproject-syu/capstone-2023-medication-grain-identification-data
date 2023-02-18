import cv2
import numpy as np
import imutils

# grayscale로 사진 바꾸는 예제
image = cv2.imread("../docs/raw_medicine_image/1cMBag.jpg")

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("ImageShow", image_gray)
cv2.waitKey(0)

import cv2
import numpy as np
import imutils

# 이미지 새 창에 띄우는 예제
image = cv2.imread("../docs/raw_medicine_image/1cMBag.jpg")
cv2.imshow("ImageShow", image)
cv2.waitKey(0)
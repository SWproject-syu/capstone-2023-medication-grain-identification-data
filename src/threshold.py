import cv2
import numpy as np
import imutils

# grayscale + blur로 사진 바꾸는 예제
image = cv2.imread("docs/raw_image/1cMBag.jpg")

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_gray_blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)


ret,thresh1 = cv2.threshold(image_gray_blurred,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(image_gray_blurred,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(image_gray_blurred,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(image_gray_blurred,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(image_gray_blurred,127,255,cv2.THRESH_TOZERO_INV)
images_row1 = np.hstack([image_gray_blurred, thresh1, thresh2])
images_row2 = np.hstack([thresh3, thresh4, thresh5])
images_combined = np.vstack((images_row1, images_row2))

cv2.imshow('Images', images_combined )
cv2.waitKey(0)
cv2.destroyAllWindows()	

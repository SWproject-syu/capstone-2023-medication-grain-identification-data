



# Import
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 알약 사진(좌우)를 2장으로 만들고 불필요한 여백을 제거합니다.
# https://youbidan.tistory.com/19
path = "docs/raw_image/" + "147427852405800073.jpg"
img = cv2.imread(path)

# Main Source
## 1. 이미지 흑백화(canny)
imgcopy = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(img, 127, 255)

contours2, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours2, -1, (255, 255, 0), 2)

# cv2.imshow('canny', canny)
# cv2.imshow('contour', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

b, g, r = cv2.split(imgcopy)
imgcopy = cv2.merge([r, g, b])
b, g, r = cv2.split(img)
img = cv2.merge([r, g, b])

titles = ['Original', 'Canny', 'Contours']
images = [imgcopy, canny, img]

plt.figure(figsize=(12, 12))
for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')
    
plt.tight_layout()
# plt.show()

## 2. 이미지 윤곽선 검출
src = img
dst = src.copy()

gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

for i in contours:
    hull = cv2.convexHull(i, clockwise=True)
    cv2.drawContours(dst, [hull], 0, (0, 0, 255), 2)

cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
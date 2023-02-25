



# Import
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from skimage.segmentation import clear_border
import skimage.morphology as mp
import scipy.ndimage as sm

# 알약 사진(좌우)를 2장으로 만들고 불필요한 여백을 제거합니다.
# https://youbidan.tistory.com/19


path = "docs/raw_image/" + "1MaQuqD9cPe.jpg"
image_origin = cv2.imread(path)
img = image_origin.copy()

# Main Source 1. Canny로 윤곽선(contours) 검출
canny1 = cv2.Canny(img, 210, 200)

# Main Source 2. 검출한 윤곽선으로 자르기
img2 = clear_border(canny1)  # 경계면을 다듬는다.

res, thr = cv2.threshold(canny1, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# 그레이 스케일로 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 이진화
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
###################
# 윤곽선 그리기
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

# 각 윤곽선을 감싸는 사각형 그리기
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 이미지 자르기
    crop = img[y:y + h, x:x + w]

    # 자른 이미지 출력
    # cv2.imshow('crop', crop)
    # cv2.waitKey(0)

# 결과 이미지 출력
cv2.imshow('contours', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
###################
plt.imshow(img2)
plt.tight_layout()
plt.show()

areas = [cv2.contourArea(cnt) for cnt in contours]
large_contours = [cnt for cnt, area in zip(contours, areas) if area > 400]
for cnt in large_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    roi = image_origin[y:y+h, x:x+w]
    plt.imshow(roi)
    plt.tight_layout()
    plt.show()








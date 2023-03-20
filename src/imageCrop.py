



# Import
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from skimage.segmentation import clear_border
import skimage.morphology as mp
import scipy.ndimage as sm
import os

# 알약 사진(좌우)를 2장으로 만들고 불필요한 여백을 제거합니다.
# https://youbidan.tistory.com/19
# 1299x709_101011_1
# 1299x709_101011_10
# 1299x709_101011_11
# 1299x709_101011_2
# 1299x709_101011_3
# 1299x709_101011_4
# 1299x709_101011_5
# 1299x709_101011_6
# 1299x709_101011_7
# 1299x709_101011_8
# 1299x709_101011_9
# 1299x709_111111
# 1299x709_12912
# 1299x709_679
# 1299x709_81012_1
# 1299x709_81012_2
# 1299x709_81012_3
# 1299x709_8912
# 1302x711_111111
# 780x424_81012
# 780x426_101011
# 780x426_12912
# 780x426_5710
# 780x426_679
# 780x426_81012
# 780x426_979
# etc
origin_dir = "780x426_81012"
path_dir = "docs/classification/"+origin_dir+"_crop_pass/"
save_dir = "docs/classification/"+origin_dir+"_crop_split/"
file_list = os.listdir(path_dir)

index = 0 
for file_name in file_list:
    index = index + 1
    # if file_name != "151326607822100097.png":
    #     continue
    
    path = path_dir + file_name
    file_basename, file_ext = os.path.splitext(file_name)
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
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    # 각 윤곽선을 감싸는 사각형 그리기
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # 이미지 자르기
        crop = img[y:y + h, x:x + w]

    areas = [cv2.contourArea(cnt) for cnt in contours]
    large_contours = contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
    # large_contours = [cnt for cnt, area in zip(contours, areas) if area > 400]
    index_crop = 0
    for cnt in large_contours:
        index_crop = index_crop + 1
        x, y, w, h = cv2.boundingRect(cnt)
        roi = image_origin[y:y+h, x:x+w]
        print('['+str(index)+'-'+str(index_crop)+']: ' + save_dir + file_basename + "_crop_" + str(index_crop) + file_ext)
        cv2.imwrite(save_dir + file_basename + "_crop_" + str(index_crop) + file_ext, roi)
        # plt.imshow(roi)
        # plt.tight_layout()
        # plt.show()

    # 이미지 저장
    print('['+str(index)+']: ' + save_dir + file_basename + "_origin_" + str(index) + file_ext)
    cv2.imwrite(save_dir + file_basename + "_origin_" + str(index) + file_ext, img)







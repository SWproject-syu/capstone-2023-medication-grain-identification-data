



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

path_dir = "docs/classification/780x424_81012_crop_pass/"
save_dir = "docs/classification/780x424_81012_crop_split/"
file_list = os.listdir(path_dir)

index = 0 
for file_name in file_list:
    index = index + 1
    # if index == 20056 or index == 20057:
    #     continue
    path = path_dir + file_name
    file_basename, file_ext = os.path.splitext(file_name)
    image_origin = cv2.imread(path)
    img = image_origin.copy()

    # Main Source 1. Canny로 윤곽선(contours) 검출
    ## History Equalization
    # hist, bins = np.histogram(img.flatten(), 256,[0,256])
    # cdf = hist.cumsum()
    # cdf_m = np.ma.masked_equal(cdf,0)
    # cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    # cdf = np.ma.filled(cdf_m,0).astype('uint8')
    # img = cdf[img]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    canny1 = cv2.Canny(gray, 210, 200)
    # Main Source 2. 검출한 윤곽선으로 자르기
    img2 = clear_border(canny1)  # 경계면을 다듬는다.

    res, thresh = cv2.threshold(canny1, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    # 그레이 스케일로 변환
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # 이진화
    # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    ###################
    img_draw = img.copy()
    
    # ######################################
    # https://stackoverflow.com/questions/66490374/how-to-merge-nearby-bounding-boxes-opencv
    # 가까운 윤곽선 합치기
    def tup(point):
        return (point[0], point[1])
    def overlap(source, target):
        tl1, br1 = source
        tl2, br2 = target
        if (tl1[0] >= br2[0] or tl2[0] >= br1[0]):
            return False
        if (tl1[1] >= br2[1] or tl2[1] >= br1[1]):
            return False
        return True
    def getAllOverlaps(boxes, bounds, index):
        overlaps = []
        for a in range(len(boxes)):
            if a != index:
                if overlap(bounds, boxes[a]):
                    overlaps.append(a)
        return overlaps
    orig = np.copy(img)
    blue, green, red = cv2.split(img)
    def medianCanny(img, thresh1, thresh2):
        median = np.median(img)
        img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
        return img
    blue_edges = medianCanny(blue, 0, 1)
    green_edges = medianCanny(green, 0, 1)
    red_edges = medianCanny(red, 0, 1)
    edges = blue_edges | green_edges | red_edges
    boxes = []
    hierarchy = hierarchy[0]
    for component in zip(contours, hierarchy):
        currentContour = component[0]
        currentHierarchy = component[1]
        x,y,w,h = cv2.boundingRect(currentContour)
        if currentHierarchy[3] < 0:
            boxes.append([[x,y], [x+w, y+h]])
    filtered = []
    max_area = 30000
    for box in boxes:
        w = box[1][0] - box[0][0]
        h = box[1][1] - box[0][1]
        if w*h < max_area:
            filtered.append(box)
    boxes = filtered
    merge_margin = 10
    finished = False
    highlight = [[0,0], [1,1]]
    points = [[[0,0]]]
    while not finished:
        finished = True
        index_func = 0
        while index_func < len(boxes):
            curr = boxes[index_func]
            tl = curr[0][:]
            br = curr[1][:]
            tl[0] -= merge_margin
            tl[1] -= merge_margin
            br[0] += merge_margin
            br[1] += merge_margin
            overlaps = getAllOverlaps(boxes, [tl, br], index_func)
            if len(overlaps) > 0:
                con = []
                overlaps.append(index_func)
                for ind in overlaps:
                    tl, br = boxes[ind]
                    con.append([tl])
                    con.append([br])
                con = np.array(con)
                x,y,w,h = cv2.boundingRect(con)
                w -= 1
                h -= 1
                merged = [[x,y], [x+w, y+h]]
                highlight = merged[:]
                points = con
                overlaps.sort(reverse = True)
                for ind in overlaps:
                    del boxes[ind]
                boxes.append(merged)
                finished = False
                break
            index_func += 1

    index_crop = 0
    for box in boxes:
        # 선 그리기
        x, y = tup(box[0])
        w, h = tup(box[1])
        if h - y < 50 or w - x < 40:
            continue
        index_crop = index_crop + 1
        # 이미지 자르기 & 자른 이미지 저장하기
        crop = img[y:h, x:w]
        print('['+str(index)+'-'+str(index_crop)+']: ' + save_dir + file_basename + "_crop_" + str(index_crop) + file_ext)
        cv2.imwrite(save_dir + file_basename + "_crop_" + str(index_crop) + file_ext, crop)
        # 선 그리기
        cv2.rectangle(img_draw, (x, y), (w, h), (0, 0, 255), 2)
        # cv2.drawContours(img_draw, cnt, -1, (0, 255, 0), 3)
    # ######################################
    # ######################################
 
    # 구분선 표시하기
    print('['+str(index)+']: ' + save_dir + file_basename + "_origin_" + str(index) + file_ext)
    cv2.imwrite(save_dir + file_basename + "_origin_" + str(index) + file_ext, img_draw)







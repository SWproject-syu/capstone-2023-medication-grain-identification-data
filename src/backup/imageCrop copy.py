



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
    # img2 = clear_border(canny1)  # 경계면을 다듬는다.

    # 그레이 스케일로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 이진화
    # res, thr = cv2.threshold(canny1, 127, 255, cv2.THRESH_BINARY)

  
    # res, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)
    # contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ###################







    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    canny1 = cv2.Canny(gray, 210, 200)
    # Main Source 2. 검출한 윤곽선으로 자르기
    img2 = clear_border(canny1)  # 경계면을 다듬는다.

    res, thresh = cv2.threshold(canny1, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # 그레이 스케일로 변환
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 이진화
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    ##################
    img_draw = img.copy()
    
    # ######################################
    # https://stackoverflow.com/questions/66490374/how-to-merge-nearby-bounding-boxes-opencv
    # 가까운 윤곽선 합치기
    
    # functions
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
    contours,hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    hierarchy = hierarchy[0]
    for component in zip(contours, hierarchy):
        currentContour = component[0]
        currentHierarchy = component[1]
        x,y,w,h = cv2.boundingRect(currentContour)
        if currentHierarchy[3] < 0:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
            boxes.append([[x,y], [x+w, y+h]])
    filtered = []
    max_area = 30000
    for box in boxes:
        w = box[1][0] - box[0][0]
        h = box[1][1] - box[0][1]
        if w*h < max_area:
            filtered.append(box)
    boxes = filtered
    merge_margin = 20
    finished = False
    highlight = [[0,0], [1,1]]
    points = [[[0,0]]]
    while not finished:
        finished = True
        # print("Len Boxes: " + str(len(boxes)))
        copy = np.copy(orig)
        for box in boxes:
            cv2.rectangle(copy, tup(box[0]), tup(box[1]), (0,255,0), 1)
        cv2.rectangle(copy, tup(highlight[0]), tup(highlight[1]), (0,0,255), 2)
        for point in points:
            point = point[0]
            cv2.circle(copy, tup(point), 4, (255,0,0), -1)
        cv2.imshow("Copy", copy)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        index_box = 0
        while index_box < len(boxes):
            curr = boxes[index_box]
            tl = curr[0][:]
            br = curr[1][:]
            tl[0] -= merge_margin
            tl[1] -= merge_margin
            br[0] += merge_margin
            br[1] += merge_margin
            overlaps = getAllOverlaps(boxes, [tl, br], index_box)
            if len(overlaps) > 0:
                con = []
                overlaps.append(index_box)
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
            index_box += 1
    plt.imshow(copy)
    plt.tight_layout()
    plt.show()
    # cv2.destroyAllWindows()
    # show final
    index_crop = 0
    copy = np.copy(orig)
    for box in boxes:
        # 선 그리기
        x, y = tup(box[0])
        w, h = tup(box[1])
        if h - y < 50 or w - x < 40:
            continue
        index_crop = index_crop + 1
        cv2.rectangle(copy, tup(box[0]), tup(box[1]), (0,255,0), 1)
        crop = img[y:h, x:w]
        print('['+str(index)+'-'+str(index_crop)+']: ' + save_dir + file_basename + "_crop_" + str(index_crop) + file_ext)
        cv2.imwrite(save_dir + file_basename + "_crop_" + str(index_crop) + file_ext, crop)
    

    # 이미지 저장
    print('['+str(index)+']: ' + save_dir + file_basename + "_origin_" + str(index) + file_ext)
    cv2.imwrite(save_dir + file_basename + "_origin_" + str(index) + file_ext, img)







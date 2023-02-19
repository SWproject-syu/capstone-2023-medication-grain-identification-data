import cv2
import numpy as np

# 이미지 불러오기
# path = "docs/raw_image/" + "154816836149000158.jpg"
path = "docs/raw_image/" + "148111442737100023.jpg"
# path = "docs/raw_image/" + "154816836149000170.jpg"
# path = "./" + "receipt_division.png"
image_origin = cv2.imread(path)

# 이미지 자르기
def cropImg(img, xscale=1.0, yscale=1.0):
    center_x, center_y = img.shape[1] / 2+55, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * xscale, img.shape[0] * yscale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2 - 20
    imgCropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return imgCropped
imgCropped = cropImg(image_origin, 1, 1)
img = imgCropped

# 특정색 삭제
def deleteColor(img):
	height, width = img.shape[:2] # 이미지의 높이와 너비 불러옴, 가로 [0], 세로[1]
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # cvtColor 함수를 이용하여 hsv 색공간으로 변환
	lower_blue = (108-10, 30, 30) # hsv 이미지에서 바이너리 이미지로 생성 , 적당한 값 30
	upper_blue = (108+10, 255, 255)
	img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue) # 범위내의 픽셀들은 흰색, 나머지 검은색
	img_mask = 255 - img_mask
	img = cv2.bitwise_and(img, img, mask = img_mask)
	return img
img = deleteColor(img)
# cv2.imshow('img_color', img)
# cv2.waitKey(0)
# exit()

# 그레이 스케일로 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 이진화
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

# 윤곽선 검출
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 특정 면적 이상만 윤곽선 그리기
areas = [cv2.contourArea(cnt) for cnt in contours]
contours = [cnt for cnt, area in zip(contours, areas) if area > 600]
cv2.drawContours(imgCropped, contours, -1, (0, 255, 0), 3)

# 가장 큰 윤곽선 2개만 남기기
def getMaxAreaIndex(contours, exceptionIndex = 0):
    max_area = 0
    index = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area > max_area and i != exceptionIndex):
            max_area = area
            index = i
    return index
ci1 = getMaxAreaIndex(contours, 0)
ci2 = getMaxAreaIndex(contours, ci1)

# 각 윤곽선을 감싸는 사각형 그리기 & 반환: 자른 이미지
def drawROI(img, contour, margin=5):    
		x, y, w, h = cv2.boundingRect(contour)
		cv2.rectangle(img, (x-margin-5, y-margin), (x + w+margin, y + h+margin), (0, 0, 255), 2)
		crop = img[y-margin:y + h+margin, x-margin-5:x + w+margin]
		return crop
cropImage1 = drawROI(imgCropped,contours[ci1])
cropImage2 = drawROI(imgCropped,contours[ci2])







# 이미지의 높이와 너비를 가져옵니다.
height, width = cropImage1.shape[:2]

# 이미지를 원하는 크기로 잘라냅니다.

# 모서리를 둥글게 하기 위한 반지름 값을 설정합니다.
radius = int(width / 2)

# 이미지의 모서리를 둥글게 만듭니다.
mask = cv2.copyMakeBorder(cropImage1, radius, radius, radius, radius, cv2.BORDER_CONSTANT)
height, width = mask.shape[:2]

# # 이미지의 높이와 너비 계산
h, w = cropImage1.shape[:2]
# 이미지 중심점 계산
center_x = int(w / 2)
center_y = int(h / 2)

for i in range(height):
    for j in range(width):
        if (i - radius - center_y) ** 2 + (j - radius - center_x) ** 2 > radius ** 2:
            mask[i, j] = [0, 0, 0]
result = mask[radius:height - radius, radius:width - radius]

# 결과 이미지를 저장합니다.
# cv2.imwrite('output_image.png', result)








# 결과 이미지 출력
cv2.imshow('contours', cropImage1)
cv2.imshow('contours', cropImage2)
cv2.imshow('contours', imgCropped)
cv2.waitKey(0)
cv2.destroyAllWindows()


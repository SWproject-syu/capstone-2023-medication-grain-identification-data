



# Import
import cv2
import numpy as np
from matplotlib import pyplot as plt

def crop_img(img, xscale=1.0, yscale=1.0):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * xscale, img.shape[0] * yscale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

# 알약 사진(좌우)를 2장으로 만들고 불필요한 여백을 제거합니다.
# https://youbidan.tistory.com/19
path = "docs/raw_image/" + "147427852405800040.jpg"
image_origin = crop_img(cv2.imread(path), 0.9, 0.6)
image = image_origin.copy()

# if w >= 100 and h >= 100:
# Main Source
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
dst = cv2.bitwise_not(image)
edged = cv2.Canny(gray, 100, 250)
(contours, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
idx = 0
for c in contours:
	x,y,w,h = cv2.boundingRect(c)
	if w>100 and h>100:
		idx+=1
		new_img=image[y:y+h,x:x+w]
		#cropping images
		cv2.imshow("Original Image",new_img)
		# cv2.imwrite("cropped/"+str(idx) + '.png', new_img)

# cv2.imshow("Original Image",dst)
cv2.imshow("Canny Edge",gray)
cv2.waitKey(0)

# Sub Process
# cv2.drawContours(new_img, contours, -1, (0, 255, 255), 2)



c0 = contours[0]
M = cv2.moments(c0)


leftmost = tuple(c0[c0[:, :, 0].argmin()][0])
rightmost = tuple(c0[c0[:, :, 0].argmax()][0])
topmost = tuple(c0[c0[:, :, 1].argmin()][0])
bottommost = tuple(c0[c0[:, :, 1].argmax()][0])

cv2.circle(new_img, (leftmost[0], leftmost[1]), 3, (0, 0, 255), -1)
cv2.circle(new_img, (rightmost[0], rightmost[1]), 3, (0, 0, 255), -1)
cv2.circle(new_img, (bottommost[0], bottommost[1]), 3, (0, 0, 255), -1)
cv2.circle(new_img, (topmost[0], topmost[1]), 3, (0, 0, 255), -1)
        
# plt.imshow(new_img)
# plt.title("Extream Point")
# plt.axis("off") 
# plt.show()

# # 2

# c1 = contours[1]
# M = cv2.moments(c1)


# leftmost = tuple(c1[c1[:, :, 0].argmin()][0])
# rightmost = tuple(c1[c1[:, :, 0].argmax()][0])
# topmost = tuple(c1[c1[:, :, 1].argmin()][0])
# bottommost = tuple(c1[c1[:, :, 1].argmax()][0])

# cv2.circle(new_img, (leftmost[0], leftmost[1]), 3, (0, 0, 255), -1)
# cv2.circle(new_img, (rightmost[0], rightmost[1]), 3, (0, 0, 255), -1)
# cv2.circle(new_img, (bottommost[0], bottommost[1]), 3, (0, 0, 255), -1)
# cv2.circle(new_img, (topmost[0], topmost[1]), 3, (0, 0, 255), -1)
        
# plt.imshow(new_img)
# plt.title("Extream Point")
# plt.axis("off")
# plt.show()
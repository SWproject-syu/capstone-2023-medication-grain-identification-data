



# Import
import cv2
import numpy as np
from matplotlib import pyplot as plt

def crop_img(img, xscale=1.0, yscale=1.0):
    center_x, center_y = img.shape[1] / 2+55, img.shape[0] / 2 + 10
    width_scaled, height_scaled = img.shape[1] * xscale, img.shape[0] * yscale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2-90
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

# 알약 사진(좌우)를 2장으로 만들고 불필요한 여백을 제거합니다.
# https://youbidan.tistory.com/19
path = "docs/raw_image/" + "147809062320700148.jpg"
image_origin = crop_img(cv2.imread(path), 1, 1)
img3 = image_origin.copy()

# Main Source
canny1 = cv2.Canny(img3, 210, 200)
canny2 = cv2.Canny(img3, 230, 200)
canny3 = cv2.Canny(img3, 250, 200)

titles = ['original', 'canny1', 'canny2', 'canny3']
images = [img3, canny1, canny2, canny3]

# cv2.imshow('original', img3)
# cv2.imshow('canny1', canny1)
# cv2.imshow('canny2', canny2)
# cv2.imshow('canny3', canny3)
cv2.waitKey(0)
cv2.destroyAllWindows()

plt.figure(figsize=(10, 10))
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.title(titles[i])
    plt.imshow(images[i], cmap='gray')
    plt.axis('off')
    
plt.tight_layout()
plt.show()
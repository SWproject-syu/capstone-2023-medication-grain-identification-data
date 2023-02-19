



# Import
import cv2
from matplotlib import pyplot as plt

# 알약 사진(좌우)를 2장으로 만들고 불필요한 여백을 제거합니다.
# https://youbidan.tistory.com/19
path = "docs/raw_image/" + "1M_4NHfUrab.jpg"
image = cv2.imread(path)

# Main Source
# import cv2
img = image
img1 = img.copy()
img2 = img.copy()
img3 = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
res, thr = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnt = contours[1]
cv2.drawContours(img, [cnt], -1, (255, 255, 0), 2)

epsilon1 = 0.05 * cv2.arcLength(cnt, True)
epsilon2 =  0.08 * cv2.arcLength(cnt, True)
epsilon3 = 0.1 * cv2.arcLength(cnt, True)

print('Original', cv2.arcLength(cnt, True))
print('epsilon 0.05', epsilon1)
print('epsilon 0.08', epsilon2)
print('epsilon 0.1', epsilon3)
print()

approx1 = cv2.approxPolyDP(cnt, epsilon1, True)
approx2 = cv2.approxPolyDP(cnt, epsilon2, True)
approx3 = cv2.approxPolyDP(cnt, epsilon3, True)

print('Original Contour 갯수', len(cnt))
print('Approx1 Contour 갯수', len(approx1))
print('Approx2 Contour 갯수', len(approx2))
print('Approx3 Contour 갯수', len(approx3))

cv2.drawContours(img1, [approx1], -1, (0, 255, 0), 3)
cv2.drawContours(img2, [approx2], -1, (0, 255, 0), 3)
cv2.drawContours(img3, [approx3], -1, (0, 255, 0), 3)

titles = ['Contours', 'Approx1 (0.05)', 'Approx2 (0.08)', 'Approx2 (0.1)']
images = [img, img1, img2, img3]
approx = [cnt, approx1, approx2, approx3]

for index in range(4):
    for i in range(len(approx[index])):
        for j in range(len(approx[index][i])):
            cv2.circle(images[index], (approx[index][i][j][0], approx[index][i][j][1]), 3, (0, 0, 255), -1)

plt.figure(figsize=(12, 12))
for i in range(4):
    plt.subplot(1, 4, i+1)
    plt.title(titles[i])
    plt.imshow(images[i])
    plt.axis('off')
    
plt.tight_layout()
plt.show()


# cv2.imshow("dst", dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
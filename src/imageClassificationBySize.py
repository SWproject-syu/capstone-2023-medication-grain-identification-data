
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
# C:\_projects\삼육대인공지능\medication-grain-identification-data\docs\raw_image\1NNuh6mJnYK.jpg
# path_dir = "docs/raw_image/"
path_dir = "docs/raw_image/"
save_dir = "docs/classification2/"
file_list = os.listdir(path_dir)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

createFolder(save_dir)
index = 0 
for file_name in file_list:
	index = index + 1
	if index == 20056 or index == 20057:
		path = path_dir + file_name
		image_origin = cv2.imread(path)
		file_basename, file_ext = os.path.splitext(file_name)
		print(file_name)
		createFolder(save_dir+'etc/')
		cv2.imwrite(save_dir+'etc/' +file_basename+file_ext, image_origin)
		continue
	# if index in range(0, 30000):
	# 	continue
	path = path_dir + file_name
	file_basename, file_ext = os.path.splitext(file_name)
	image_origin = cv2.imread(path)

	# 하단 footer 기준 이미지 분리
	h, w = image_origin.shape[:2]
	b,g,r = image_origin[h-10][10]

	# image_origin[h-10][10] = (255, 0, 0)
	footer_rgb = str(round(r/20))+str(round(g/20))+str(round(b/20))
	size = str(w)+'x'+str(h)
	size_footer_folder_path = size + "_" + footer_rgb

	save_path = save_dir + size_footer_folder_path
	createFolder(save_path)
	cv2.imwrite(save_path +'/'+ file_basename+file_ext, image_origin)
	print(index)

	
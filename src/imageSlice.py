



# Import
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from skimage.segmentation import clear_border
import skimage.morphology as mp
import scipy.ndimage as sm
import os

origin_dir = "780x426_81012_crop_pass"
path_dir = "docs/classification/"+origin_dir+"/psd_019/"
save_dir = "docs/classification/"+origin_dir+"/_crop_split_psd_019/"
file_list = os.listdir(path_dir)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

index = 0 
for file_name in file_list:
    index = index + 1
    # if file_name != "151326607822100097.png":
        # continue
    path = path_dir + file_name
    file_basename, file_ext = os.path.splitext(file_name)
    image_origin = cv2.imread(path)
    img = image_origin.copy()

    createFolder(save_dir)

    h, w = img.shape[:2]

    slice_1 = img[0:h, 0:(w//2)]
    # print('[1/2]: ' + save_dir + file_basename + "_slice1" + file_ext)
    cv2.imwrite(save_dir + file_basename + "_slice1" + file_ext, slice_1)

    slice_2 = img[0:h, (w//2):w]
    # print('[2/2]: ' + save_dir + file_basename + "_slice2" + file_ext)
    cv2.imwrite(save_dir + file_basename + "_slice2" + file_ext, slice_2)

    # 이미지 저장
    print('['+str(index)+']: ' + save_dir + file_basename + "_origin_" + str(index) + file_ext)
    cv2.imwrite(save_dir + file_basename + "_origin_" + str(index) + file_ext, img)







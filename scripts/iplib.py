# -*- coding: utf-8 -*-
import numpy as np
import cv2

threshold = 127

def binarize(image):
    ret, img_thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    #cv2.imshow("img_th", img_thresh)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    cv2.imwrite('thresh_image.jpg', img_thresh)
    return img_thresh

def object_detection(image):
    grid_0x = []
    splited_image = split_image(image)
    for i in splited_image:
        grid_0x.append(calc_binary_rate(i))
        if calc_binary_rate(i) > 90:
            i.fill(255)
        else:
            i.fill(0)
    ################# to graphical view
    hage = np.reshape(splited_image,(6,10,120,120))
    im_tile = concat_tile(hage)
    cv2.imwrite('result.jpg',im_tile)
    #################

    return grid_0x

def crop(image):
    height, width = image.shape
    #buff = int((width-height)/2)
    buff = int(80/2)
    cropped_image = image[0:height,buff:width-buff]
    return cropped_image

def box_detection(img,temp):
    #マッチングテンプレートを実行
    #比較方法はcv2.TM_CCOEFF_NORMEDを選択
    result = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)

    #検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    w, h = temp.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    #検出領域を四角で囲んで保存
    result = cv2.imread("sample_cropped_fixed_marked_02.jpg",0)
    result.fill(0)
    cv2.rectangle(result,top_left, bottom_right, 255, -1)
    
    cv2.imwrite("templete_matching_result.png", result)

    splited_image = split_image(result)
    existing_rate = []
    for i in splited_image:
        existing_rate.append(int(calc_binary_rate(i)))

    return existing_rate


def split_image(image):
    grid_size = 120
    splited_image = []
    grid_0x = []
    height, width = image.shape

    height_split = int(height/grid_size)
    width_split = int(width/grid_size)
    new_img_height = int(height / height_split)
    new_img_width = int(width / width_split)

    for h in range(height_split):
        height_start = h * new_img_height
        height_end = height_start + new_img_height

        for w in range(width_split):
            width_start = w * new_img_width
            width_end = width_start + new_img_width

            #file_name = "test_" + str(h) + "_" + str(w) + ".png"
            clp = image[height_start:height_end, width_start:width_end]
            #cv2.imwrite(file_name, clp)
            splited_image.append(clp)
    return splited_image


def calc_binary_rate(image):
    image_size = image.size
    white_pixels = cv2.countNonZero(image)
    black_pixels = image.size - white_pixels
    
    white_rate = (white_pixels / image_size)*100

    return white_rate

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

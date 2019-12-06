# -*- coding: utf-8 -*-
import numpy as np
import cv2

import iplib

class ObstacleController():
    def __init__(self):
        pass

    def predict(self, hoge):
        image = cv2.resize(cv2.imread('sample_cropped_fixed_marked_02.jpg',0),(1280,720))
        templete = cv2.imread('template_resized.png',0)

        image = iplib.crop(image)
        binary_image = iplib.binarize(image)
        box_existing_map = iplib.box_detection(image,templete)
        #box_existing_map = np.reshape(box_existing_map,(6,10))

        obstacle_map = iplib.object_detection(binary_image)

        hoge = []
        for rate in obstacle_map:
            if rate > 90:
                hoge.append(True)
            else:
                hoge.append(False)

        # ゴミ箱のいるところを障害物なしとして処理する
        i = 0
        for e_rate in box_existing_map:
            if e_rate > 10:
                hoge[i] = True
            i+=1

        hoge = np.reshape(hoge,(6,10))
        box_existing_map = np.reshape(box_existing_map,(6,10))

        print('-------------map-------------')
        print(hoge)
        print('-----box rocation-----')
        print(box_existing_map)
        return None



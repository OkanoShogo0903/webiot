# -*- coding: utf-8 -*-
import numpy as np
import cv2

import iplib

class ObstacleController():
    def __init__(self):
        pass

    def predict(self):
        image = cv2.resize(cv2.imread('sample_cropped_fixed_marked.jpg',0),(1280,720))
        templete = cv2.imread('template_resized.png',0)

        #ゴミ箱の座標を取得
        image = iplib.crop(image)
        box_existing_map = iplib.box_detection(image,templete)

        #障害物マップを生成
        binary_image = iplib.binarize(image)
        obstacle_map = iplib.object_detection(binary_image)

        #グリッド内の白ピクセルが90%以上なら障害物なしとして判定
        obstacle_grid_map = []
        for rate in obstacle_map:
            if rate > 90:
                obstacle_grid_map.append(True)
            else:
                obstacle_grid_map.append(False)

        # ゴミ箱のいるところを障害物なしとして処理する
        i = 0
        for e_rate in box_existing_map:
            if e_rate > 10:
                obstacle_grid_map[i] = True
            i+=1

        #各マップを2次元配列に再構成
        obstacle_grid_map = np.reshape(obstacle_grid_map,(6,10))
        box_existing_map = np.reshape(box_existing_map,(6,10))
        
        box_grid = np.where(box_existing_map == np.amax(box_existing_map))

        #結果の出力
        print('-------------map-------------')
        print(obstacle_grid_map)
        print('-----box rocation-----')
        print(box_existing_map)
        print(box_grid)
        return (obstacle_grid_map, box_grid)

test_instance = ObstacleController()
test_instance.predict()


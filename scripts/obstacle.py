# -*- coding: utf-8 -*-
import numpy as np
import cv2

import iplib

class ObstacleController():
    def __init__(self):
        pass

    def predict(self,image):
        #image = cv2.resize(cv2.imread('sample_cropped_fixed_marked.jpg',0),(1280,720))
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image,(1280,720))
            
        templete = cv2.imread('mark.jpeg',0)
        image = iplib.crop(image)

        #ゴミ箱の座標を取得
        #box_existing_map = iplib.box_detection(image,templete)
        box_point, box_angle = iplib.get_ar(image)
        if box_point is None:
            return None,None,None,None
        box_angle = float(box_angle.strip('['']'))*(-1)
        #print(type(box_angle))
        box_existing_map = iplib.box_point_to_grid(image,box_point)

        #障害物マップを生成
        binary_image = iplib.binarize(image)
        obstacle_map = iplib.object_detection(binary_image)

        #グリッド内の白ピクセルが90%以上なら障害物なしとして判定
        obstacle_grid_map = []
        for rate in obstacle_map:
            if rate > 90:
                obstacle_grid_map.append(0)
            else:
                obstacle_grid_map.append(1)

        # ゴミ箱のいるところを障害物なしとして処理する
        i = 0
        for e_rate in box_existing_map:
            if e_rate is 1:
            #if e_rate > 10:
                obstacle_grid_map[i] = 0
            i+=1

        #各マップを2次元配列に再構成
        obstacle_grid_map = np.reshape(obstacle_grid_map,(6,10))
        box_existing_map = np.reshape(box_existing_map,(6,10))
        #padding
        obstacle_grid_map = np.pad(obstacle_grid_map,(1,1), 'constant',constant_values=(1,1))
        box_existing_map = np.pad(box_existing_map,(1,1), 'constant',constant_values=(0,0))
        
        box_grid = np.where(box_existing_map == np.amax(box_existing_map))
        box_grid = [box_grid[0][0],box_grid[1][0]]


        return (obstacle_grid_map, box_grid, box_point, box_angle)
        '''
        obstacle_grid_map: 障害物マップ（グリッド）
        box_gird：ゴミ箱の存在位置(グリッド)
        box_point：ゴミ箱の存在位置（座標）
        box_angle：ゴミ箱の向いている角度
        '''

if __name__ == '__main__':

    test_instance = ObstacleController()
    image = cv2.resize(cv2.imread('rotate_sample.jpg'),(1280,720))
    obstacle_grid_map, box_grid, box_point, box_angle = test_instance.predict(image)
    if obstacle_grid_map is not None:
        print('-------------map-------------')
        print(obstacle_grid_map)
        print('-----box grid-----')
        print(box_grid)
        print('-----box angle-----')
        print(box_angle)
        print('-----box point-----')
        print(box_point)
    else:
        print('missing box')


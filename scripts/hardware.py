# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages') # For avoid reference to ROS's opencv.
import cv2

class HardwareController():
    def __init__(self, cap, grid_size):
        self.grid_x_pix = grid_size
        self.grid_y_pix = grid_size


    def predict(self, direction_grid_x, direction_grid_y, hardware_pix_x, hardware_pix_y, hardware_degree):
        """
        座標系変換 : http://www.mech.tohoku-gakuin.ac.jp/rde/contents/course/robotics/coordtrans.html
        degreeは3時方向を0[deg], 12時方向を90[deg]とする.

        >>> import numpy as np
        >>> hardware_controller = HardwareController(0, 120)
        >>> hardware_controller.predict(1, 0, 60, 60, 0)
        array([120.,   0.])
        >>> hardware_controller.predict(1, 0, 60, 120, 0)
        array([120., -60.])
        >>> hardware_controller.predict(1, 0, 60, 120, 270)
        array([ -60., -120.])
        """
        # Convert hardware pix to grid.
        target_pix_x = direction_grid_x * self.grid_x_pix + (self.grid_x_pix/2)
        target_pix_y = direction_grid_y * self.grid_y_pix + (self.grid_y_pix/2)
        target_vector = np.array( [ target_pix_x, target_pix_y ]) - np.array( [ hardware_pix_x, hardware_pix_y ] )

        # 座標系変換 ( グローバル座標系 -> ロボット座標系 )
        t = np.deg2rad(hardware_degree)
        a = np.array([[np.cos(t), -np.sin(t)],
                    [np.sin(t),  np.cos(t)]])
        ax = np.dot(a, target_vector)  
        return ax


if __name__ == '__main__':

    grid_size = 120

    device = 0
    cap = cv2.VideoCapture(device)

    direction_grid_x = 1
    direction_grid_y = 0
    hardware_x = 60
    hardware_y = 120

    hardware_controller = HardwareController(cap, grid_size)
    k = hardware_controller.predict(direction_grid_x, direction_grid_y, hardware_x, hardware_y, 270)

# -*- coding: utf-8 -*-
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages') # For avoid reference to ROS's opencv.
import cv2

import json
import time
import numpy as np
import requests as m5_requests
import threading

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, abort
from flask_api import status

import obstacle
import route_search
import hardware
import mqtt_pub


app = Flask(__name__)

goal_x, goal_y = None, None

image = None
device = 0
grid_size = 120
cap = cv2.VideoCapture(device)

obstacle_controller = obstacle.ObstacleController()
route_controller = route_search.RouteController()
hardware_controller = hardware.HardwareController(cap, grid_size)
mqtt = mqtt_pub.MqttPublisher()


@app.route('/goal', methods=['POST'])
def goal():
    """
        @discription:
            APIが呼び出されるとゴールとなるグリッドの座標を更新する。
    """
    try:
        global goal_x # グローバル使ってごめんなさい
        global goal_y
        goal_x = request.form["x"]
        goal_y = request.form["y"]
        return make_response("ok-" + goal_x + "-" + goal_y)
    except:
        import traceback
        traceback.print_exc()


@app.route("/healthcheck", methods=['GET'])
def healthcheck():
    return make_response("ok")


def instruction(img, goal_grid_x, goal_grid_y):
    """
        @discription:
            制御対象が指定されているグリッドに向かうための制御情報を送る役目
    """
    hardware_x = 60
    hardware_y = 120
    rotate = 270

    i = obstacle_controller.predict(img)
    next_grid_coordinate = route_controller.predict()

    send_pix_xy = hardware_controller.predict(
           next_grid_coordinate[0],
           next_grid_coordinate[1],
           hardware_x,
           hardware_y,
           rotate
           )

    mqtt.publish(str(int(send_pix_xy[0]))+","+str(int(send_pix_xy[1])))


def imageRenew():
    global image
    if not cap.isOpened():
        return
    _, image = cap.read()


def schedule(interval, f, args=None, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        if args == None:
            t = threading.Thread(target=f)
        else:
            t = threading.Thread(target=f, args=args)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
    cap.release()


if __name__ == '__main__':
    # 画像データの更新
    image_thread = threading.Thread(
            target=schedule,
            args=(0.1, imageRenew)
            )
    image_thread.start()

    # ユーザから指示されるゴールグリッドの更新
    api_thread = threading.Thread(
            target=app.run,
            args=("0.0.0.0", 5000)
            )
    api_thread.start()

    # ゴールグリッドへ制御対象を向かわせるためのデータ更新
    instruction_thread = threading.Thread(
            target=schedule,
            args=(0.3, instruction, (image, goal_x, goal_y))
            )
    instruction_thread.start()

    # メインスレッドはプログラムの終了を待つ
    instruction_thread.join()

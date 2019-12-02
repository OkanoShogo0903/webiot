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


app = Flask(__name__)

goal_x, goal_y = None, None

image = None
device = 0
cap = cv2.VideoCapture(device)

obstacle_controller = obstacle.ObstacleController()
route_controller = route_search.RouteController()
hardware_controller = hardware.HardwareController()


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
    i = obstacle_controller.predict(img)
    j = route_controller.predict(i)
    k = hardware_controller.predict(j)
    
    try:
        m5_requests.post(
                'http://0.0.0.0:1234/post',
                {'foo':'bar'}) 
    except m5_requests.exceptions.ConnectionError:
        print('ConnectionError: Check M5 Stack connection')


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

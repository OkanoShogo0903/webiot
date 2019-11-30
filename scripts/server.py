# -*- coding: utf-8 -*-
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages') # For avoid reference to ROS's opencv.
import cv2

import time
import numpy as np
import threading

from flask import Flask, render_template, request, redirect, url_for

import obstacle
import route_search
import hardware

app = Flask(__name__)
image = None
device = 0
cap = cv2.VideoCapture(device)

obstacle_controller = obstacle.ObstacleController()
route_controller = route_search.RouteController()
hardware_controller = hardware.HardwareController()

@app.route('/get', methods=['GET'])
def get():
    try:
        i = obstacle_controller.predict(image)
        j = route_controller.predict(i)
        k = hardware_controller.predict(i)
        res = {"demo": k}
        return make_response(jsonify(res))
    except:
        import traceback
        traceback.print_exc()


@app.route("/healthcheck", methods=['GET'])
def healthcheck():
    return make_response("ok")


def imageRenew():
    global image
    if not cap.isOpened():
        return
    _, image = cap.read()


def schedule(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
    cap.release()


if __name__ == '__main__':
    image_thread = threading.Thread(
            target=schedule,
            args=(0.1, imageRenew)
            )
    image_thread.start()

    app.run(host="0.0.0.0", port=5000)


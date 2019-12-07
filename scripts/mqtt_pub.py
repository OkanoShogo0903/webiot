# -*- coding: utf-8 -*-

from struct import *
from time import sleep
import paho.mqtt.client as mqtt

class MqttPublisher(object):
    def __init__(self, host = '127.0.0.1', port = 1883, topic = 'f_team/direction'):
        # インスタンス作成時に protocol v3.1.1 を指定します
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.topic = topic

        self.client.connect(host, port=port, keepalive=60)

    def publish(self, msg):
        self.client.publish(self.topic, msg)

    def __del__(self):
        self.client.disconnect()

if __name__ == '__main__':
    m = MqttPublisher()
    m.publish("100,200")

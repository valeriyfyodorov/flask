import os
import re
import requests
import urllib.request as urequest
import time
import numpy as np
import json
from socket import timeout
import urllib.parse
import cv2  # run opencv_install.sh to install
# from picamera import PiCamera
from PIL import Image
from random import randint
import zbarlight
from pyModbusTCP.client import ModbusClient

SCALES_NAME_FOR_ID = {"2": "north", "1": "south"}
TRAFFIC_LIGHT_API_URL = "http://192.168.21.82:8123/api/services/mqtt/publish"
TRAFFIC_LIGHT_API_AUTH = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxYTQ2NjM1ZmI3NWU0NmI1YmIzMzU2NjkzYzViYzg4YyIsImlhdCI6MTYzODk2OTA1NCwiZXhwIjoxOTU0MzI5MDU0fQ.ib-WYqlTWzzLsM3PVCLLkS6_0bVIc5G8f1GI_YI3VUI"
SCALES = {
    "north":
    {
        "id": 2,
        "cam_front":
        {
            "url": "rtsp://192.168.20.183:554/video2",
            "crop_ratio": [0.3, 0.97, 0.255, 0.99],
            "warp_from": [[400, 400], [500, 400], [500, 500], [400, 500]],
            "warp_to": [[400, 400], [500, 400], [500, 500], [400, 500]],
        },
        "cam_rear":
        {
            "url": "rtsp://192.168.20.184:554/video2",
            "crop_ratio": [0.39, 0.81, 0.35, 0.8],
            "warp_from": [[400, 400], [500, 400], [500, 500], [400, 500]],
            "warp_to": [[400, 400], [500, 400], [500, 500], [400, 500]],
        },
        "cam_top":
        {
            "url": "rtsp://192.168.20.185:554/video2",
            "crop_ratio": [0.5, 0.7, 0.4, 0.6],
            "warp_from": [[528, 332], [528, 355], [631, 354], [631, 332]],
            "warp_to": [[528, 332], [528, 355], [631, 354], [631, 332]],
        },
        "modbus":
        {
            "host": "192.168.21.124",
            "port": 505,
        },
        "light_topic_front": "trafficlights/ts2ftl/status",
        "light_topic_rear": "trafficlights/ts2rtl/status",
    },
    "south":
    {
        "id": 1,
        "cam_front":
        {
            "url": "rtsp://192.168.20.180:554/video2",
            "crop_ratio": [0.3, 0.97, 0.255, 0.99],
            "warp_from": [[400, 400], [500, 400], [500, 500], [400, 500]],
            "warp_to": [[400, 400], [500, 400], [500, 500], [400, 500]],
        },
        "cam_rear":
        {
            "url": "rtsp://192.168.20.181:554/video2",
            "crop_ratio": [0.39, 0.81, 0.35, 0.8],
            "warp_from": [[400, 400], [500, 400], [500, 500], [400, 500]],
            "warp_to": [[400, 400], [500, 400], [500, 500], [400, 500]],
        },
        "cam_top":
        {
            "url": "rtsp://192.168.20.182:554/video2",
            "crop_ratio": [0.3, 0.5, 0.3, 0.5],
            "warp_from": [[528, 332], [528, 355], [631, 354], [631, 332]],
            "warp_to": [[528, 332], [528, 355], [631, 354], [631, 332]],
        },
        "modbus":
        {
            "host": "192.168.21.124",
            "port": 504,
        },
        "light_topic_front": "trafficlights/ts1ftl/status",
        "light_topic_rear": "trafficlights/ts1rtl/status",
    },
}


def switchTrafficLight(scaleId, payload="green", topic="light_topic_front"):
    scaleId = str(scaleId)
    scale = SCALES[SCALES_NAME_FOR_ID[scaleId]]
    body = {"payload": payload, "topic": scale[topic]}
    req = urequest.Request(TRAFFIC_LIGHT_API_URL)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Authorization', TRAFFIC_LIGHT_API_AUTH)
    jsondataasbytes = json.dumps(body).encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    try:
        with urequest.urlopen(req, jsondataasbytes) as response:
            if response.getcode() == 200:
                source = response.read()
                if len(source) > 0:
                    result = json.loads(source)
                else:
                    print(
                        'switchTrafficLight. When trying to read data from server API zero length response received')
            else:
                print(
                    'switchTrafficLight. An error occurred while attempting to retrieve lists data from the API.')
    except timeout:
        print(
            'switchTrafficLight. Timeout error when trying API call'
        )
    return result


def switchBothTrafficLight(scaleId, payload="green"):
    topic = "light_topic_front"
    switchTrafficLight(scaleId, payload, topic)
    topic = "light_topic_rear"
    return switchTrafficLight(scaleId, payload, topic)


print(switchBothTrafficLight("2"))

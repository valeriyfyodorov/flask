from .utils import Timer
from .config import SCALES, ALPR_API_TOKEN, ALPR_URL, DEBUG_WITH_DUMMY_PLATES, DUMMY_IMG_FRONT
import re
import requests
import numpy as np
import cv2 # run opencv_install.sh to install

def bad_image(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv],[1],None,[5],[0,180])
    return min(hist) / max(hist) < 0.001

def unskewed_image(img, box_warped, box_straight):
    image[np.where(image == 0)] = 1
    height = img.shape[0]
    width = img.shape[1]
    TM = cv2.getPerspectiveTransform(box_warped, box_straight)
    warped = cv2.warpPerspective(img, TM, (img.shape[1],img.shape[0]))
    warped[np.where(warped == 0)] = img[np.where(warped == 0)]
    return warped

def readRtspImage(scale_cam, trials=5):
    address = scale_cam["url"]
    crop_ratio = scale_cam["crop_ratio"]
    box_from = np.float32(scale_cam["warp_from"])
    box_to = np.float32(scale_cam["warp_to"])
    vcap = None
    frame = None
    for x in range(trials):
        try:
            vcap = cv2.VideoCapture(address)
            break
        except:
            print(f"readRtspImage. Failed to open Videocapture for {address}")
            continue
    timer = Timer("camRead")
    while True:
        try:
            ret, frame = vcap.read()
            if not bad_image(frame) or timer.read() > 5 : break
        except:
            print(f"readRtspImage. Failed to capture image at {address}")
            break
    vcap.release()
    if frame is None:
        return frame
    height = frame.shape[0]
    width = frame.shape[1]
    frame = unskewed_image(frame, box_from, box_to)
    cropped = frame[
        int(height*crop_ratio[0]):int(height*crop_ratio[1]), 
        int(width*crop_ratio[2]):int(width*crop_ratio[3])
    ]
    if DEBUG_WITH_DUMMY_PLATES:
        cropped = cv2.imread(DUMMY_IMG_FRONT)
    return cropped

def chooseBestFromAPI(input_array):
    exclusions = ['mb533', 'wb533']
    pattern = r'^[a-zA-Z]+\d+'
    result = ""
    for item in input_array:
        item = item['plate']
        if not item:
            continue
        item = item.strip().lower().replace(' ', '').replace('-', '')
        if item in exclusions:
            continue
        if len(item) > 7:
            continue
        if re.search(pattern, item):
            return item.upper()
    return result

def recognizePlate(img):
    if img is None: return ""
    result = ""
    headers = {'Authorization': ALPR_API_TOKEN}
    is_success, img_buffer = cv2.imencode(".jpg", img)
    img_encoded = img_buffer.tostring()
    try:
        files = {'upload': img_encoded}
        response = requests.post(ALPR_URL, files=files, headers=headers)
        if (len(response.json()['results']) != 0):
            result = chooseBestFromAPI(response.json()['results'])
    except:
        print("Error during plate getting from api")
    return result



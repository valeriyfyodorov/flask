MAC_OS = True
MAC_TEST_LOCATION = '/Users/Valera/Documents/venprojs/pi/latest/html/'

if MAC_OS:
    from . import GPIO
else:
    import RPi.GPIO as GPIO

DEBUG_WITH_DUMMY_SCALES = False
DEBUG_WITH_DUMMY_INVOICE = False
DEBUG_WITH_DUMMY_PLATES = False
DEBUG_WITH_DUMMY_QR = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_BUZZER = 26
GPIO.setup(GPIO_BUZZER, GPIO.OUT)
GPIO.output(GPIO_BUZZER, False)

GPIO_LAMP = 22
GPIO.setup(GPIO_LAMP, GPIO.OUT)
GPIO.output(GPIO_LAMP, False)

CHECK_SAMPLER_HOMING = True

# ls /dev/video* first for right camera device here, minus 1 means first working
VIDEO_CAPTURE_DEVICE = -1
WEBCAM_BUFFER_SIZE = 5
WEBCAM_COLD_START = False
global video_capture

IMAGES_DIRECTORY = '/var/www/html/'
if MAC_OS:
    IMAGES_DIRECTORY = MAC_TEST_LOCATION

DUMMY_IMG_FRONT = IMAGES_DIRECTORY + 'dummy-front.jpg'
DUMMY_IMG_REAR = IMAGES_DIRECTORY + 'dummy-rear.jpg'
DUMMY_IMG_INVOICE = IMAGES_DIRECTORY + 'dummy-invoice.jpg'
DUMMY_IMG_QR = IMAGES_DIRECTORY + 'dummy-qr.jpg'
TEMP_INVOICE_IMG_FILE = IMAGES_DIRECTORY + 'invoice.jpg'
TEMP_PLATE_IMG_FILE_FRONT = IMAGES_DIRECTORY + 'front.jpg'
TEMP_PLATE_IMG_FILE_REAR = IMAGES_DIRECTORY + 'rear.jpg'

DB_SERVER_URL = "https://backup.amgs.me/autoweight/"
DB_SERVER_API_URL = "http://amgs.me/apijson.ashx?key=gd3784h67hxgugb"

ALPR_API_TOKEN = 'Token 702d66a3f614a31139fefd757892acfb85771ee7'
ALPR_URL = 'https://backup.platerecognizer.com/v1/plate-reader'

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
        "sampler_homing_gpio_port": 24,
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
        "sampler_homing_gpio_port": 23,
    },
}


class PlatesSet:
    def __init__(self, front="", rear=""):
        self.front = front
        self.rear = rear
        self.full = f"{{front}}/{{rear}}"

    def __str__(self):
        return f"front: {self.front} rear: {self.rear}"

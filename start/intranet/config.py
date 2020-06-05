import .GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_BUZZER = 26
GPIO.setup(GPIO_BUZZER, GPIO.OUT)
GPIO.output(GPIO_BUZZER, False)

GPIO_LAMP = 22
GPIO.setup(GPIO_LAMP, GPIO.OUT)
GPIO.output(GPIO_LAMP, False)


class PlatesSet:
    front = ""
    rear = ""
    def __init__(self, front="", rear=""):
        self.front = front
        self.rear = rear
        self.full = f"{{front}}/{{rear}}"


MAC_OS = True

VIDEO_CAPTURE_DEVICE = -1 # ls /dev/video* first for right camera device here, minus 1 means first working
USE_PI_CAMERA_FOR_WEBCAM = False # for qr code
WEBCAM_BUFFER_SIZE = 5

WEBCAM_COLD_START = False

PLATES_DIRECTORY = '/var/www/html/'
ALPR_API_TOKEN = 'Token 702d66a3f614a31139fefd757892acfb85771ee7'
ALPR_URL = 'https://api.platerecognizer.com/v1/plate-reader'

SCALES = {
    "north":
    {
        "cam_front": 
        {
            "url": "rtsp://192.168.21.113:554/video2",
            "crop_ratio": [0.61, 0.97, 0.255, 0.99],
        },
        "cam_rear": 
        {
            "url": "rtsp://192.168.21.114:554/video2",
            "crop_ratio": [0.39, 0.81, 0.35, 0.8],
        },
        "modbus": 
        {
            "host": "192.168.21.124",
            "port": 504,
        },
    },
    "south":
    {
        "cam_front": 
        {
            "url": "rtsp://192.168.21.113:554/video2",
            "crop_ratio": [0.61, 0.97, 0.255, 0.99],
        },
        "cam_rear": 
        {
            "url": "rtsp://192.168.21.114:554/video2",
            "crop_ratio": [0.39, 0.81, 0.35, 0.8],
        },
        "modbus": 
        {
            "host": "192.168.21.124",
            "port": 504,
        },
    },
}


MAC_TEST_LOCATION = '/Users/Valera/Documents/venprojs/pi/'
MAC_TEST_COMMAND = '/Users/Valera/Documents/venprojs/pi/snapshot_mac.sh'

global video_capture
MAC_OS = True
MAC_TEST_LOCATION = '/Users/Valera/Documents/venprojs/pi/latest/html/'

if MAC_OS:
    from . import GPIO
else:
    import RPi.GPIO as GPIO

DEBUG_WITH_DUMMY_SCALES = True
DEBUG_WITH_DUMMY_INVOICE = True
DEBUG_WITH_DUMMY_PLATES = True
DEBUG_WITH_DUMMY_QR = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_BUZZER = 26
GPIO.setup(GPIO_BUZZER, GPIO.OUT)
GPIO.output(GPIO_BUZZER, False)

GPIO_LAMP = 22
GPIO.setup(GPIO_LAMP, GPIO.OUT)
GPIO.output(GPIO_LAMP, False)

VIDEO_CAPTURE_DEVICE = -1 # ls /dev/video* first for right camera device here, minus 1 means first working
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

ALPR_API_TOKEN = 'Token 702d66a3f614a31139fefd757892acfb85771ee7'
ALPR_URL = 'https://api.platerecognizer.com/v1/plate-reader'

SCALES_NAME_FOR_ID = {"0": "north", "1": "south"}
SCALES = {
    "north":
    {
        "id": 0,
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
        "id": 1,
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

class PlatesSet:
    def __init__(self, front="", rear=""):
        self.front = front
        self.rear = rear
        self.full = f"{{front}}/{{rear}}"
    
    def __str__(self): 
        return f"front: {self.front} rear: {self.rear}"

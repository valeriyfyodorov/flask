from pyModbusTCP.client import ModbusClient
from shutil import copyfile
import cv2
import zbarlight
from .utils import Timer, archiveFileName, dictFromArgs
from .config import PlatesSet, SCALES, DEBUG_WITH_DUMMY_SCALES, SCALES_NAME_FOR_ID, IMAGES_DIRECTORY, TEMP_INVOICE_IMG_FILE
from .vision import recognizePlate, readRtspImage
from .picam import captureInvoiceToFile, camToPilImg

def getPlatesNumbers(scalesName):
    plates = PlatesSet()
    img_front = readRtspImage(
            SCALES[scalesName]["cam_front"]["url"], 
            crop_ratio=SCALES[scalesName]["cam_front"]["crop_ratio"]
        )
    plates.front = recognizePlate(img_front)
    img_rear = readRtspImage(
            SCALES[scalesName]["cam_rear"]["url"],
            crop_ratio=SCALES[scalesName]["cam_rear"]["crop_ratio"]
        )
    plates.rear = recognizePlate(img_rear)
    if len(plates.front) > 8:
        plates.front = plates.front[-6:]
    if len(plates.rear) > 8:
        plates.rear = "S" + plates.rear[-4:]
    return plates

def getWeightKg(scalesName):
    c = ModbusClient()
    c.host(SCALES[scalesName]["modbus"]["host"])
    c.port(SCALES[scalesName]["modbus"]["port"])
    if not c.is_open():
        if not c.open():
            print(f"unable to connect to modbus {SCALES[scalesName]['modbus']['host']} at port {SCALES[scalesName]['modbus']['port']}")
    str_weight = "0"            
    if c.is_open():
        regs = c.read_holding_registers(1, 1)
        if regs:
            str_weight = str(regs)[1: -1].strip()
    if c.is_open():
        c.close() # close connection on every weight request
    result = int(str_weight)
    if result == 0 and DEBUG_WITH_DUMMY_SCALES:
        if scalesName == "north": result = 44000
        if scalesName == "south": result = 9000
    return result

def readInvoice():
    timer = Timer("invoice")
    result = False
    number = ""
    while True:
        # TODO real qr recognition here
        result, number = captureInvoiceToFile()
        if result or timer.read() > 10 : break # 10 seconds to try to scan invoice
    return result, number

def archivePlates(car_id, args):
    queryDict = dictFromArgs(args)
    wkg= str(queryDict["wkg"])
    ptf = str(queryDict["ptf"]).replace('/', '-').replace('\\', '-')
    ptr = str(queryDict["ptr"]).replace('/', '-').replace('\\', '-')
    sc = str(queryDict["sc"]).strip()
    scalesName = SCALES_NAME_FOR_ID[sc]
    img_front = readRtspImage(
            SCALES[scalesName]["cam_front"]["url"], 
            crop_ratio=SCALES[scalesName]["cam_front"]["crop_ratio"]
        )
    img_rear = readRtspImage(
            SCALES[scalesName]["cam_rear"]["url"],
            crop_ratio=SCALES[scalesName]["cam_rear"]["crop_ratio"]
        )
    cv2.imwrite(archiveFileName(IMAGES_DIRECTORY, f"_{car_id}_({wkg}-F-{ptf}).jpg"),img_front)
    cv2.imwrite(archiveFileName(IMAGES_DIRECTORY, f"_{car_id}_({wkg}-R-{ptr}).jpg"),img_rear)


def archiveInvoice(car_id, args, invoiceNr):
    queryDict = dictFromArgs(args)
    wkg= str(queryDict["wkg"])
    copyfile(TEMP_INVOICE_IMG_FILE, archiveFileName(IMAGES_DIRECTORY, f"_{car_id}_({wkg}-#{invoiceNr}).jpg"))


def readQrCodeFromCam():
    timer = Timer("readqr")
    code = 0
    while True:
        codes = zbarlight.scan_codes(['qrcode'], camToPilImg())
        print(codes)
        if codes is not None:
            code = int(codes[0])
        if code > 0 or timer.read() > 10 : break
    return code
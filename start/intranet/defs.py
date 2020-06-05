from .utils import Timer

def readQrCodeFromCam():
    timer = Timer("readqr")
    code = 0
    while True:
        # TODO real qr recognition here
        code = 42339
        if code > 0 or timer.read() > 5 : break
    return code

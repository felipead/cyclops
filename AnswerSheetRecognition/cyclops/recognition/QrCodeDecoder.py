from subprocess import check_output, CalledProcessError
import os

from cv2 import imwrite

class QrCodeDecoder:

    __QR_CODE_FILENAME = "./qrcode.png"
    __ZBAR_EXECUTABLE = "zbarimg"
    __ZBAR_RAW_OUTPUT_OPTION = "--raw"

    def __init__(self):
        pass

    def decode(self, qrCodeFrame):
        qrCodePictureFile = self.__savePicture(qrCodeFrame.projectedPicture)
        try:
            output = None
            with open(os.devnull, 'w') as nullOut:
                subprocessArguments = [self.__ZBAR_EXECUTABLE, self.__ZBAR_RAW_OUTPUT_OPTION, qrCodePictureFile]
                rawOutput = check_output(subprocessArguments, stderr=nullOut)
                output = self.__extractQrCodeValue(rawOutput)
            return output
        except CalledProcessError:
            return None

    def __savePicture(self, picture):
        imwrite(self.__QR_CODE_FILENAME, picture)
        return self.__QR_CODE_FILENAME

    def __extractQrCodeValue(self, output):
        lines = output.split('\n')
        return lines[0]
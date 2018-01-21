from subprocess import check_output, CalledProcessError
import os
from cv2 import imwrite

from .QrCodeData import *

class QrCodeDecoder:

    __QR_CODE_FILENAME = "./qrcode.png"
    __ZBAR_EXECUTABLE = "zbarimg"
    __ZBAR_RAW_OUTPUT_OPTION = "--raw"

    def __init__(self):
        pass

    def decode(self, qrCodeFrame):
        qrCodePictureFile = self.__savePicture(qrCodeFrame.projectedPicture)
        try:
            qrCodeData = None
            with open(os.devnull, 'w') as nullOut:
                subprocessArguments = [self.__ZBAR_EXECUTABLE, self.__ZBAR_RAW_OUTPUT_OPTION, qrCodePictureFile]
                processOutput = check_output(subprocessArguments, stderr=nullOut)
                qrCodeString = self._extractQrCodeString(processOutput)
                if qrCodeString != None:
                    qrCodeData = self._extractQrCodeData(qrCodeString)
            return qrCodeData
        except CalledProcessError:
            return None

    def __savePicture(self, picture):
        imwrite(self.__QR_CODE_FILENAME, picture)
        return self.__QR_CODE_FILENAME

    def _extractQrCodeString(self, binary):
        text = binary.decode('utf-8')
        lines = text.split()
        return lines[0]

    def _extractQrCodeData(self, qrCodeString):
        qrCode = QrCodeData()
        qrCode.rawString = qrCodeString
        # TODO: remove hard-coded values, parse string
        qrCode.numberOfQuestions = 20
        qrCode.numberOfAnswerChoices = 5
        qrCode.numberOfQuestionsPerColumn = 10
        return qrCode

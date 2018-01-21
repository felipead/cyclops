from subprocess import check_output, CalledProcessError
import os
import cv2

from .QrCodeData import *


class QrCodeDecoder:

    __QR_CODE_FILENAME = './qrcode.png'
    __ZBAR_EXECUTABLE = 'zbarimg'
    __ZBAR_RAW_OUTPUT_OPTION = '--raw'

    def __init__(self):
        pass

    def decode(self, qr_code_frame):
        picture_file = self.__save_picture(qr_code_frame.projected_picture)
        try:
            qr_code_data = None
            with open(os.devnull, 'w') as null_out:
                process_arguments = [self.__ZBAR_EXECUTABLE, self.__ZBAR_RAW_OUTPUT_OPTION, picture_file]
                process_output = check_output(process_arguments, stderr=null_out)
                qr_code_string = self._extract_qr_code_string(process_output)
                if qr_code_string is not None:
                    qr_code_data = self._extract_qr_code_data(qr_code_string)
            return qr_code_data
        except CalledProcessError:
            return None

    def __save_picture(self, picture):
        cv2.imwrite(self.__QR_CODE_FILENAME, picture)
        return self.__QR_CODE_FILENAME

    def _extract_qr_code_string(self, binary):
        text = binary.decode('utf-8')
        lines = text.split()
        return lines[0]

    def _extract_qr_code_data(self, qr_code_string):
        qr_code = QrCodeData()
        qr_code.raw_string = qr_code_string
        # TODO: remove hard-coded values, parse string
        qr_code.number_questions = 20
        qr_code.number_answer_choices = 5
        qr_code.number_questions_per_column = 10
        return qr_code

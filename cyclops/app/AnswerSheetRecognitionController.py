import cv2

from ..recognition.AnswerSheetRecognizer import *
from ..util.DrawingUtil import *
from ..util.ImageProcessingUtil import *


_MAIN_PICTURE_WINDOW_NAME = 'main'
_ANSWER_SHEET_PICTURE_WINDOW_NAME = 'answer sheet'
_QR_CODE_PICTURE_WINDOW_NAME = 'qr code'
_BLANK_IMAGE = ImageProcessingUtil.create_blank_image(1, 1)


class AnswerSheetRecognitionController:

    def __init__(self):
        self._recognizer = AnswerSheetRecognizer()

    def init(self):
        cv2.namedWindow(_MAIN_PICTURE_WINDOW_NAME)
        cv2.namedWindow(_ANSWER_SHEET_PICTURE_WINDOW_NAME)
        cv2.namedWindow(_QR_CODE_PICTURE_WINDOW_NAME)

    def process_picture(self, picture):
        result = self._recognizer.recognize(picture)

        if result.answer_frame is not None:
            DrawingUtil.draw_quadrilateral_lines(
                picture, result.answer_frame.original_quadrilateral, DrawingUtil.COLOR_RED, 1
            )
            DrawingUtil.draw_quadrilateral_lines(
                picture, result.qr_code_frame.original_quadrilateral, DrawingUtil.COLOR_RED, 1
            )
            if result.qr_code_data is not None:
                print(result.qr_code_data)
            else:
                print('unable to capture qr code!')

        picture = cv2.flip(picture, 1)

        cv2.imshow(_MAIN_PICTURE_WINDOW_NAME, picture)
        if result.answer_frame is not None:
            cv2.imshow(_ANSWER_SHEET_PICTURE_WINDOW_NAME, result.answer_frame.projected_picture)
            cv2.imshow(_QR_CODE_PICTURE_WINDOW_NAME, result.qr_code_frame.projected_picture)
        else:
            cv2.imshow(_ANSWER_SHEET_PICTURE_WINDOW_NAME, _BLANK_IMAGE)
            cv2.imshow(_QR_CODE_PICTURE_WINDOW_NAME, _BLANK_IMAGE)

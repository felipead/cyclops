import cv2;

from ..recognition.AnswerSheetRecognizer import *
from ..util.DrawingUtil import *
from ..util.ImageProcessingUtil import *

class AnswerSheetRecognitionController:

    _MAIN_PICTURE_WINDOW_NAME = "main"
    _ANSWER_SHEET_PICTURE_WINDOW_NAME = "answer sheet"
    _QR_CODE_PICTURE_WINDOW_NAME = "qr code"
    _BLANK_IMAGE = ImageProcessingUtil.createBlankImage(1,1)

    def __init__(self):
        self._answerSheetRecognizer = AnswerSheetRecognizer()

    def init(self):
        cv2.namedWindow(self._MAIN_PICTURE_WINDOW_NAME)
        cv2.namedWindow(self._ANSWER_SHEET_PICTURE_WINDOW_NAME)
        cv2.namedWindow(self._QR_CODE_PICTURE_WINDOW_NAME)

    def processPicture(self, picture):
        
        result = self._answerSheetRecognizer.recognize(picture)

        if result.answerFrame != None:
            DrawingUtil.drawQuadrilateralLines(picture, result.answerFrame.originalQuadrilateral, DrawingUtil.COLOR_RED, 1)            
            DrawingUtil.drawQuadrilateralLines(picture, result.qrCodeFrame.originalQuadrilateral, DrawingUtil.COLOR_RED, 1)
            if result.qrCodeData != None:
                print result.qrCodeData
            else:
                print "unable to capture qr code!"

        picture = cv2.flip(picture, 1);

        cv2.imshow(self._MAIN_PICTURE_WINDOW_NAME, picture)
        if result.answerFrame != None:
            cv2.imshow(self._ANSWER_SHEET_PICTURE_WINDOW_NAME, result.answerFrame.projectedPicture)
            cv2.imshow(self._QR_CODE_PICTURE_WINDOW_NAME, result.qrCodeFrame.projectedPicture)
        else:
            cv2.imshow(self._ANSWER_SHEET_PICTURE_WINDOW_NAME, self._BLANK_IMAGE)
            cv2.imshow(self._QR_CODE_PICTURE_WINDOW_NAME, self._BLANK_IMAGE)

from cv2 import namedWindow, imshow, flip, waitKey, VideoCapture

from ..recognition.AnswerSheetRecognizer import *
from ..recognition.AnswerSheetRecognitionResult import *

MAIN_PICTURE_WINDOW_NAME = "main"
ANSWER_SHEET_PICTURE_WINDOW_NAME = "answer sheet"
QR_CODE_PICTURE_WINDOW_NAME = "qr code"

def readCamera(camera):
    _, picture = camera.read()
    return picture


def execute():
    namedWindow(MAIN_PICTURE_WINDOW_NAME)
    namedWindow(ANSWER_SHEET_PICTURE_WINDOW_NAME)
    namedWindow(QR_CODE_PICTURE_WINDOW_NAME)
    camera = VideoCapture(0)

    mainPicture = readCamera(camera)

    while True:

        if mainPicture != None:
            recognizer = AnswerSheetRecognizer()
            recognitionResult = recognizer.recognize(mainPicture)

            mainPicture = flip(mainPicture, 1);
            imshow(MAIN_PICTURE_WINDOW_NAME, mainPicture)
            if recognitionResult.answerSheetFrame != None:
                imshow(ANSWER_SHEET_PICTURE_WINDOW_NAME, recognitionResult.answerSheetFrame.projectedPicture)
                imshow(QR_CODE_PICTURE_WINDOW_NAME, recognitionResult.qrCodeFrame.projectedPicture)
        
        mainPicture = readCamera(camera)

        if waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    execute()
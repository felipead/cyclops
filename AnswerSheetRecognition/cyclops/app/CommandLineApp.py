import sys
from sys import stdin

from cv2 import imshow, namedWindow, flip

from ..recognition.AnswerSheetRecognizer import *

MAIN_PICTURE_WINDOW_NAME = "main"
ANSWER_SHEET_PICTURE_WINDOW_NAME = "answer sheet"
QR_CODE_PICTURE_WINDOW_NAME = "qr code"

def execute():
    if len(sys.argv) != 2:
        print "Missing picture file as argument"
        return

    mainPicture = imread(sys.argv[1])
    mainPicture = flip(mainPicture, 1);

    if mainPicture != None:
        namedWindow(MAIN_PICTURE_WINDOW_NAME)
        namedWindow(ANSWER_SHEET_PICTURE_WINDOW_NAME)
        namedWindow(QR_CODE_PICTURE_WINDOW_NAME)

        recognizer = AnswerSheetRecognizer()
        recognitionResult = recognizer.recognize(mainPicture)

        imshow(MAIN_PICTURE_WINDOW_NAME, mainPicture)
        if recognitionResult.answerSheetFrame != None:
            imshow(ANSWER_SHEET_PICTURE_WINDOW_NAME, recognitionResult.answerSheetFrame.projectedPicture)
            imshow(QR_CODE_PICTURE_WINDOW_NAME, recognitionResult.qrCodeFrame.projectedPicture)

        raw_input("Press Enter to exit...")
    else:
        print "Invalid picture"


if __name__ == "__main__":
    execute()
from cv2 import namedWindow, imshow, flip, waitKey, VideoCapture

from ..recognition.AnswerSheetRecognizer import *

MAIN_PICTURE_WINDOW_NAME = "main"
ANSWER_SHEET_PICTURE_WINDOW_NAME = "answer sheet"

def readCamera(camera):
    _, picture = camera.read()
    picture = flip(picture, 1);
    return picture


def execute():
    namedWindow(MAIN_PICTURE_WINDOW_NAME)
    namedWindow(ANSWER_SHEET_PICTURE_WINDOW_NAME)
    camera = VideoCapture(0)

    mainPicture = readCamera(camera)

    while True:

        if mainPicture != None:
            recognizer = AnswerSheetRecognizer()
            answerSheetPicture = recognizer.recognize(mainPicture)
            imshow(MAIN_PICTURE_WINDOW_NAME, mainPicture)
            if answerSheetPicture != None:
                imshow(ANSWER_SHEET_PICTURE_WINDOW_NAME, answerSheetPicture)
        
        mainPicture = readCamera(camera)

        if waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    execute()
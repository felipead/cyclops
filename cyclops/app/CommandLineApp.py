import sys
from sys import stdin

from cv2 import flip

from .AnswerSheetRecognitionController import *


def execute():
    if len(sys.argv) != 2:
        print("Missing picture file as argument")
        return 1

    picture = imread(sys.argv[1])
    if picture is None:
        print("Invalid picture")
        return 1

    picture = flip(picture, 1)
    controller = AnswerSheetRecognitionController()
    controller.init()
    controller.processPicture(picture)
    print('Press any key inside the OpenCV window to quit...')
    cv2.waitKey()

    return 0

if __name__ == "__main__":
    execute()

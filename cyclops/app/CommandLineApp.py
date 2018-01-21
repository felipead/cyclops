import sys
from sys import stdin
import cv2

from .AnswerSheetRecognitionController import *


def main():
    if len(sys.argv) != 2:
        print('Missing picture file as argument')
        return 1

    picture = cv2.imread(sys.argv[1])
    if picture is None:
        print('Invalid picture')
        return 1

    picture = cv2.flip(picture, 1)
    controller = AnswerSheetRecognitionController()
    controller.init()
    controller.process_picture(picture)
    print('Press any key inside the OpenCV window to quit...')
    cv2.waitKey()


if __name__ == '__main__':
    main()

import sys
from sys import stdin

from cv2 import flip

from AnswerSheetRecognitionController import *


def execute():
    if len(sys.argv) != 2:
        print "Missing picture file as argument"
        return 1

    picture = imread(sys.argv[1])
    if picture == None:
        print "Invalid picture"
        return 1

    picture = flip(picture, 1)
    controller = AnswerSheetRecognitionController()
    controller.init()
    controller.processPicture(picture)

    raw_input("Press Enter to exit...")
    return 0        

if __name__ == "__main__":
    execute()
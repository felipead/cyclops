import sys
from sys import stdin

from cv2 import imshow

from ..recognition.AnswerSheetRecognizer import *


def execute():
    if len(sys.argv) != 2:
        print "Missing picture file as argument"
        return
    
    picture = imread(sys.argv[1])

    if picture != None:
        recognizer = AnswerSheetRecognizer()
        recognizer.recognize(picture)
        imshow("cyclops", picture)
        raw_input("Press Enter to exit...")
    else:
        print "Invalid picture"


if __name__ == "__main__":
    execute()
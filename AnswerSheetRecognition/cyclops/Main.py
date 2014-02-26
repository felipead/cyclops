import sys
from sys import stdin

from cv2 import *

from AnswerSheetRecognizer import *

class Main:

    @staticmethod
    def execute():
        if len(sys.argv) != 2:
            print "Missing picture as argument"
            return
        
        picture = imread(sys.argv[1])

        recognizer = AnswerSheetRecognizer()
        recognizer.recognize(picture)

        imshow("cyclops", picture)
        raw_input("Press Enter to exit...")


if __name__ == "__main__":
    Main().execute()
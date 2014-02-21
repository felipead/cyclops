import sys
from sys import stdin

from cv2 import *

from FrameExtractor import *

class Main:

    @staticmethod
    def execute():
        if len(sys.argv) != 6:
            print "Insufficient number of arguments"
            return
        
        picture = imread(sys.argv[1])
        circleTemplate1 = imread(sys.argv[2]);
        circleTemplate2 = imread(sys.argv[3]);
        ballTemplate1 = imread(sys.argv[4]);
        ballTemplate2 = imread(sys.argv[5]);

        frameExtractor = FrameExtractor([circleTemplate1, circleTemplate2], [ballTemplate1, ballTemplate2]);
        frameExtractor.matchAllTemplatesAgainst(picture)

        imshow("picture", picture)
        input("Press Enter to continue...")


if __name__ == "__main__":
    Main().execute()
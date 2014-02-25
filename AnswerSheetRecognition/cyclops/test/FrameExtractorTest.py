from unittest import *

from ..FrameExtractor import *

from ..MathUtil import *

from cv2 import *
import math

class FrameExtractorTest(TestCase):

    def setUp(self):
        self.frameExtractor = FrameExtractor()

    def testFindSquareInListOfPoints(self):
        assert self.frameExtractor._findSquareInListOfPoints(basePoint=(424, 312), \
            otherPoints=[(505, 104), (295, 23), (214, 236), (587, 250), (338, 88), (298, 194)], error=5) == [(424,312), (505,104), (295,23), (214,236)]


if __name__ == "__main__":
    unittest.main()

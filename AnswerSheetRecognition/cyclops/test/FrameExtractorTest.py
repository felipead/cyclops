from unittest import *

from ..FrameExtractor import *

from ..MathUtil import *

from cv2 import *
import math

class FrameExtractorTest(TestCase):

    def setUp(self):
        self.frameExtractor = FrameExtractor()

    def testFindSquareInListOfPoints1(self):
        basePoint=(424, 312)
        otherPoints=[(505, 104), (295, 23), (214, 236), (587, 250), (338, 88), (298, 194)]
        error=5
        assert self.frameExtractor._findSquareInListOfPoints(basePoint, otherPoints, error) == [(424, 312), (505, 104), (295, 23), (214, 236)]

    def testFindSquareInListOfPoints2(self):
        basePoint=(490, 342)
        otherPoints=[(549, 239), (122, 252), (184, 258), (525, 71), (248, 45), (228, 313)]
        error=10
        assert self.frameExtractor._findSquareInListOfPoints(basePoint, otherPoints, error) == [(490, 342), (525, 71), (248, 45), (228, 313)]


if __name__ == "__main__":
    unittest.main()

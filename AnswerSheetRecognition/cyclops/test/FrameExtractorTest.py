from unittest import *

from ..FrameExtractor import *
from ..MathUtil import *
from ..QuadrilateralPolygon import *

import math

class FrameExtractorTest(TestCase):

    def setUp(self):
        self.frameExtractor = FrameExtractor()

    def testFindQuadrilateralInListOfPoints1(self):
        basePoint=(424, 312)
        otherPoints=[(505, 104), (295, 23), (214, 236), (587, 250), (338, 88), (298, 194)]
        sizeRelaxationRatio=1.08
        assert self.frameExtractor._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints, sizeRelaxationRatio)[0] == QuadrilateralPolygon([(424, 312), (505, 104), (295, 23), (214, 236)])

    def testFindQuadrilateralInListOfPoints2(self):
        basePoint=(490, 342)
        otherPoints=[(549, 239), (122, 252), (184, 258), (525, 71), (248, 45), (228, 313)]
        sizeRelaxationRatio=1.08
        assert self.frameExtractor._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints, sizeRelaxationRatio)[0] == QuadrilateralPolygon([(490, 342), (525, 71), (248, 45), (228, 313)])

if __name__ == "__main__":
    unittest.main()

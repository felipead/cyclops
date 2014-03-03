from unittest import *

from ..FrameExtractor import *
from ..MathUtil import *
from ..QuadrilateralPolygon import *

import math

class FrameExtractorTest(TestCase):

    def setUp(self):
        self.sizeRelaxationRatio = 1.08
        self.angleRelaxationInRadians = 0.15
        self.frameExtractor = FrameExtractor(self.sizeRelaxationRatio, self.angleRelaxationInRadians)

    def testFindQuadrilateralInListOfPoints1(self):
        basePoint=(424, 312)
        otherPoints=[(505, 104), (295, 23), (214, 236), (587, 250), (338, 88), (298, 194)]
        assert list(self.frameExtractor._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints))[0] ==\
            QuadrilateralPolygon([(424, 312), (505, 104), (295, 23), (214, 236)], self.angleRelaxationInRadians)

    def testFindQuadrilateralInListOfPoints2(self):
        basePoint=(490, 342)
        otherPoints=[(549, 239), (122, 252), (184, 258), (525, 71), (248, 45), (228, 313)]
        assert list(self.frameExtractor._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints))[0] ==\
            QuadrilateralPolygon([(490, 342), (525, 71), (248, 45), (228, 313)], self.angleRelaxationInRadians)

if __name__ == "__main__":
    unittest.main()

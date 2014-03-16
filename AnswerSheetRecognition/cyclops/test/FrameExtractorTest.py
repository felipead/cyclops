from unittest import *

from ..recognition.FrameExtractor import *
from ..util.MathUtil import *
from ..geometry.ConvexQuadrilateral import *
from ..pattern.PatternMatch import *

import math

class FrameExtractorTest(TestCase):

    def setUp(self):
        self.sizeRelaxationRatio = 1.10
        self.angleRelaxationInRadians = 0.2
        self.frameExtractor = FrameExtractor(self.sizeRelaxationRatio, self.angleRelaxationInRadians)


    def testFindConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(self):
        basePoint=(125, 98)
        otherPoints=[(135, 327), (359, 333), (364, 99), (552, 210), (285, 169), (362, 99)]
        quadrilaterals = self.frameExtractor._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints)
        assert ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (364, 99)]) in quadrilaterals
        assert ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (362, 99)]) in quadrilaterals
        for quadrilateral in quadrilaterals:
            assert quadrilateral.hasRightInteriorAnglesWithRelaxationOf(self.angleRelaxationInRadians)


    def testFindFramesSample01(self):
        matchSize = (32,32)
        frameOrientationMatches = self.buildPatternMatches([(37, 266), (492, 343)], matchSize)
        frameAlignmentMatches = self.buildPatternMatches([(142, 16), (622, 371), (190, 259), (526, 72), (248, 45), (228, 314)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(492, 343), (526, 72), (248, 45), (228, 314)]))
        self.findFramesTestRunner(frameOrientationMatches, frameAlignmentMatches, expectedFrames)

    def testFindFramesSample02(self):
        matchSize = (32,32)
        frameOrientationMatches = self.buildPatternMatches([(624, 161), (519, 368)], matchSize)
        frameAlignmentMatches = self.buildPatternMatches([(169, 353), (89, 397), (80, 397), (216, 370), (538, 56), (204, 56)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(519, 368), (538, 56), (204, 56), (216, 370)]))
        self.findFramesTestRunner(frameOrientationMatches, frameAlignmentMatches, expectedFrames)

    def testFindFramesSample03(self):
        matchSize = (32,32)
        frameOrientationMatches = self.buildPatternMatches([(526, 363), (519, 364)], matchSize)
        frameAlignmentMatches = self.buildPatternMatches([(171, 344), (89, 303), (81, 309), (535, 54), (213, 51), (218, 362)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(526, 363), (535, 54), (213, 51), (218, 362)]))
        expectedFrames.append(ConvexQuadrilateral([(519, 364), (535, 54), (213, 51), (218, 362)]))
        self.findFramesTestRunner(frameOrientationMatches, frameAlignmentMatches, expectedFrames)

    def testFindFramesSample04(self):
        matchSize = (32,32)
        frameOrientationMatches = self.buildPatternMatches([(180, 368), (580, 239)], matchSize)
        frameAlignmentMatches = self.buildPatternMatches([(417, 360), (417, 130), (182, 127), (119, 159), (481, 195), (251, 205)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(180, 368), (417, 360), (417, 130), (182, 127)]))
        self.findFramesTestRunner(frameOrientationMatches, frameAlignmentMatches, expectedFrames)

    def testFindFramesSample05(self):
        matchSize = (32,32)
        frameOrientationMatches = self.buildPatternMatches([(125, 98), (121, 96)], matchSize)
        frameAlignmentMatches = self.buildPatternMatches([(135, 327), (359, 333), (364, 99), (552, 210), (285, 169), (362, 99)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(121, 96), (135, 327), (359, 333), (362, 99)]))
        expectedFrames.append(ConvexQuadrilateral([(121, 96), (135, 327), (359, 333), (364, 99)]))
        expectedFrames.append(ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (364, 99)]))
        expectedFrames.append(ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (362, 99)]))
        self.findFramesTestRunner(frameOrientationMatches, frameAlignmentMatches, expectedFrames)

    
    def findFramesTestRunner(self, frameOrientationMatches, frameAlignmentMatches, expectedFrames):
        foundFrames = self.frameExtractor._findAnswerSheetQuadrilaterals(frameOrientationMatches, frameAlignmentMatches)
        for expectedFrame in expectedFrames:
            assert expectedFrame in foundFrames

    def buildPatternMatches(self, centers, size):
        matches = []
        for center in centers:
            matches.append(PatternMatch.fromCenter(center, size))
        return matches


if __name__ == "__main__":
    unittest.main()

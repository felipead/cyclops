from unittest import *

from ..recognition.AnswerFrameExtractor import *
from ..util.MathUtil import *
from ..geometry.ConvexQuadrilateral import *
from ..pattern.PatternMatch import *


class AnswerFrameExtractorTest(TestCase):

    def setUp(self):
        self.sizeRelaxationRatio = 1.10
        self.angleRelaxationInRadians = 0.2
        self.answerFrameExtractor = AnswerFrameExtractor(self.sizeRelaxationRatio, self.angleRelaxationInRadians)


    def testFindConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(self):
        basePoint=(125, 98)
        otherPoints=[(135, 327), (359, 333), (364, 99), (552, 210), (285, 169), (362, 99)]
        quadrilaterals = self.answerFrameExtractor._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints)
        assert ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (364, 99)]) in quadrilaterals
        assert ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (362, 99)]) in quadrilaterals
        for quadrilateral in quadrilaterals:
            assert quadrilateral.hasRightInteriorAnglesWithRelaxationOf(self.angleRelaxationInRadians)


    def testFindAnswerFrameQuadrilateralsSample01(self):
        matchSize = (32,32)
        frameOrientationPatternMatches = self.buildPatternMatches([(37, 266), (492, 343)], matchSize)
        frameAlignmentPatternMatches = self.buildPatternMatches([(142, 16), (622, 371), (190, 259), (526, 72), (248, 45), (228, 314)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(492, 343), (526, 72), (248, 45), (228, 314)]))
        self.findAnswerFramesQuadrilateralsTestRunner(frameOrientationPatternMatches, frameAlignmentPatternMatches, expectedFrames)

    def testFindAnswerFrameQuadrilateralsSample02(self):
        matchSize = (32,32)
        frameOrientationPatternMatches = self.buildPatternMatches([(624, 161), (519, 368)], matchSize)
        frameAlignmentPatternMatches = self.buildPatternMatches([(169, 353), (89, 397), (80, 397), (216, 370), (538, 56), (204, 56)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(519, 368), (538, 56), (204, 56), (216, 370)]))
        self.findAnswerFramesQuadrilateralsTestRunner(frameOrientationPatternMatches, frameAlignmentPatternMatches, expectedFrames)

    def testFindAnswerFrameQuadrilateralsSample03(self):
        matchSize = (32,32)
        frameOrientationPatternMatches = self.buildPatternMatches([(526, 363), (519, 364)], matchSize)
        frameAlignmentPatternMatches = self.buildPatternMatches([(171, 344), (89, 303), (81, 309), (535, 54), (213, 51), (218, 362)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(526, 363), (535, 54), (213, 51), (218, 362)]))
        expectedFrames.append(ConvexQuadrilateral([(519, 364), (535, 54), (213, 51), (218, 362)]))
        self.findAnswerFramesQuadrilateralsTestRunner(frameOrientationPatternMatches, frameAlignmentPatternMatches, expectedFrames)

    def testFindAnswerFrameQuadrilateralsSample04(self):
        matchSize = (32,32)
        frameOrientationPatternMatches = self.buildPatternMatches([(180, 368), (580, 239)], matchSize)
        frameAlignmentPatternMatches = self.buildPatternMatches([(417, 360), (417, 130), (182, 127), (119, 159), (481, 195), (251, 205)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(180, 368), (417, 360), (417, 130), (182, 127)]))
        self.findAnswerFramesQuadrilateralsTestRunner(frameOrientationPatternMatches, frameAlignmentPatternMatches, expectedFrames)

    def testFindAnswerFrameQuadrilateralsSample05(self):
        matchSize = (32,32)
        frameOrientationPatternMatches = self.buildPatternMatches([(125, 98), (121, 96)], matchSize)
        frameAlignmentPatternMatches = self.buildPatternMatches([(135, 327), (359, 333), (364, 99), (552, 210), (285, 169), (362, 99)], matchSize)
        expectedFrames = []
        expectedFrames.append(ConvexQuadrilateral([(121, 96), (135, 327), (359, 333), (362, 99)]))
        expectedFrames.append(ConvexQuadrilateral([(121, 96), (135, 327), (359, 333), (364, 99)]))
        expectedFrames.append(ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (364, 99)]))
        expectedFrames.append(ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (362, 99)]))
        self.findAnswerFramesQuadrilateralsTestRunner(frameOrientationPatternMatches, frameAlignmentPatternMatches, expectedFrames)
    
    def findAnswerFramesQuadrilateralsTestRunner(self, frameOrientationPatternMatches, frameAlignmentPatternMatches, expectedFrames):
        foundFrames = self.answerFrameExtractor._findAnswerFrameQuadrilaterals(frameOrientationPatternMatches, frameAlignmentPatternMatches)
        for expectedFrame in expectedFrames:
            assert expectedFrame in foundFrames

    def buildPatternMatches(self, centers, size):
        matches = []
        for center in centers:
            matches.append(PatternMatch.fromCenter(center, size))
        return matches


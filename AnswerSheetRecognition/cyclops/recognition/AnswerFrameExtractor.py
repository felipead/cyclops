import math

from AnswerFrameExtractionResult import *
from Frame import *

from ..pattern.FrameAlignmentPatternMatcher import *
from ..pattern.FrameOrientationPatternMatcher import *

from ..geometry.Vector import *
from ..geometry.ConvexQuadrilateral import *
from ..geometry.Square import *
from ..util.MathUtil import *
from ..util.PerspectiveUtil import *

class AnswerFrameExtractor:

    __ANSWER_SHEET_QUADRILATERAL_SCALE = 1.15


    def __init__(self, sizeRelaxationRatio=1.10, angleRelaxationInRadians=0.3):
        self._sizeRelaxationRatio = sizeRelaxationRatio
        self._angleRelaxationInRadians = angleRelaxationInRadians
        self._frameAlignmentPatternMatcher = FrameAlignmentPatternMatcher()
        self._frameOrientationPatternMatcher = FrameOrientationPatternMatcher()


    def extract(self, picture):
        frameOrientationPatternMatches = self._frameOrientationPatternMatcher.match(picture, 1)
        frameAlignmentPatternMatches = self._frameAlignmentPatternMatcher.match(picture, 3)

        answerFrameQuadrilaterals = self._findAnswerFrameQuadrilaterals(frameOrientationPatternMatches, frameAlignmentPatternMatches)
        bestAnswerFrameQuadrilateral = None
        if answerFrameQuadrilaterals != []:
            bestAnswerFrameQuadrilateral = self._chooseQuadrilateralThatBestResemblesSquare(answerFrameQuadrilaterals)

        answerFrame = None
        if bestAnswerFrameQuadrilateral != None:
            answerFrame = self.__extractAnswerFrame(picture, bestAnswerFrameQuadrilateral)

        return self.__buildResult(answerFrame, answerFrameQuadrilaterals, frameOrientationPatternMatches, frameAlignmentPatternMatches)


    def __buildResult(self, answerFrame, answerFrameQuadrilaterals, frameOrientationPatternMatches, frameAlignmentPatternMatches):
        result = AnswerFrameExtractionResult()
        result.frameOrientationPatternMatches = frameOrientationPatternMatches
        result.frameAlignmentPatternMatches = frameAlignmentPatternMatches
        if answerFrame != None:
            result.answerFrame = answerFrame
            answerFrameMismatches = answerFrameQuadrilaterals
            answerFrameMismatches.remove(answerFrame.originalQuadrilateral)
            result.answerFrameMismatches = answerFrameMismatches
        return result


    def _findAnswerFrameQuadrilaterals(self, frameOrientationPatternMatches, frameAlignmentPatternMatches):
        otherPoints = []
        for frameAlignmentMatch in frameAlignmentPatternMatches:
            otherPoints.append(frameAlignmentMatch.center)

        quadrilaterals = set()
        for frameOrientationMatch in frameOrientationPatternMatches:
            basePoint = frameOrientationMatch.center
            quadrilaterals.update(self._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints))

        return list(quadrilaterals)

    def _findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(self, basePoint, otherPoints):
        convexQuadrilaterals = set()

        for firstPoint in otherPoints:
            baseDistance = MathUtil.distanceBetweenPoints(firstPoint, basePoint)
            for secondPoint in otherPoints:
                if secondPoint == firstPoint:
                    continue                    
                if self.__areDistancesRoughlyEqual(MathUtil.distanceBetweenPoints(firstPoint, secondPoint), baseDistance):
                    for thirdPoint in otherPoints:
                        if thirdPoint == firstPoint or thirdPoint == secondPoint:
                            continue    
                        if self.__areDistancesRoughlyEqual(MathUtil.distanceBetweenPoints(secondPoint, thirdPoint), baseDistance):
                            if self.__areDistancesRoughlyEqual(MathUtil.distanceBetweenPoints(thirdPoint, basePoint), baseDistance):
                                points = (basePoint, firstPoint, secondPoint, thirdPoint)
                                quadrilateral = self.__getConvexQuadrilateralWithRoughlyRightInteriorAngles(points)
                                if quadrilateral != None:
                                    convexQuadrilaterals.add(quadrilateral)

        return convexQuadrilaterals

    def __getConvexQuadrilateralWithRoughlyRightInteriorAngles(self, points):
        polygon = Polygon(points)
        if polygon.isConvex:
            convexQuadrilateral = ConvexQuadrilateral(polygon.vertexes)
            if convexQuadrilateral.hasRightInteriorAnglesWithRelaxationOf(self._angleRelaxationInRadians):
                return convexQuadrilateral
        return None

    def __areDistancesRoughlyEqual(self, distance1, distance2):
        return MathUtil.equalWithinRatio(distance1, distance2, self._sizeRelaxationRatio)


    def _chooseQuadrilateralThatBestResemblesSquare(self, frames):
        # TODO
        return frames[0]

    def __extractAnswerFrame(self, picture, quadrilateral):
        scaledQuadrilateral = quadrilateral.scaledBy(self.__ANSWER_SHEET_QUADRILATERAL_SCALE)
        counterclockwiseQuadrilateral = scaledQuadrilateral.asCounterclockwise()

        projectionSize = int(counterclockwiseQuadrilateral.largestSideLength)
        projectionSquare = ConvexQuadrilateral([(projectionSize-1, projectionSize-1), (0, projectionSize-1), (0, 0), (projectionSize-1, 0)])

        projectedAnswerFramePicture = PerspectiveUtil.projectQuadrilateralToSquarePicture(picture, counterclockwiseQuadrilateral, projectionSquare)
        
        frame = Frame()
        frame.originalQuadrilateral = quadrilateral
        frame.scaledQuadrilateral = scaledQuadrilateral
        frame.originalPicture = picture
        frame.projectedPicture = projectedAnswerFramePicture
        return frame

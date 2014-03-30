import math

from AnswerSheetFrameExtractionResult import *
from Frame import *

from ..pattern.FrameAlignmentPatternMatcher import *
from ..pattern.FrameOrientationPatternMatcher import *

from ..geometry.Vector import *
from ..geometry.ConvexQuadrilateral import *
from ..geometry.Square import *
from ..util.MathUtil import *
from ..util.PerspectiveUtil import *

class AnswerSheetFrameExtractor:

    __ANSWER_SHEET_QUADRILATERAL_SCALE = 1.15


    def __init__(self, sizeRelaxationRatio=1.10, angleRelaxationInRadians=0.3):
        self._sizeRelaxationRatio = sizeRelaxationRatio
        self._angleRelaxationInRadians = angleRelaxationInRadians
        self._frameAlignmentMatcher = FrameAlignmentPatternMatcher()
        self._frameOrientationMatcher = FrameOrientationPatternMatcher()


    def extract(self, picture):
        frameOrientationMatches = self._frameOrientationMatcher.match(picture, 1)
        frameAlignmentMatches = self._frameAlignmentMatcher.match(picture, 3)

        answerSheetQuadrilaterals = self._findAnswerSheetQuadrilaterals(frameOrientationMatches, frameAlignmentMatches)
        bestAnswerSheetQuadrilateral = None
        if answerSheetQuadrilaterals != []:
            bestAnswerSheetQuadrilateral = self._chooseQuadrilateralThatBestResemblesSquare(answerSheetQuadrilaterals)

        answerSheetFrame = None
        if bestAnswerSheetQuadrilateral != None:
            answerSheetFrame = self.__extractAnswerSheetFrame(picture, bestAnswerSheetQuadrilateral)

        return self.__buildResult(frameOrientationMatches, frameAlignmentMatches, answerSheetQuadrilaterals, answerSheetFrame)


    def __buildResult(self, frameOrientationMatches, frameAlignmentMatches, answerSheetQuadrilaterals, answerSheetFrame):
        result = AnswerSheetFrameExtractionResult()
        result.frameOrientationMatches = frameOrientationMatches
        result.frameAlignmentMatches = frameAlignmentMatches
        if answerSheetFrame != None:
            result.answerSheetMatchFrame = answerSheetFrame
            answerSheetMismatchQuadrilaterals = answerSheetQuadrilaterals
            answerSheetMismatchQuadrilaterals.remove(answerSheetFrame.originalQuadrilateral)
            result.answerSheetMismatchQuadrilaterals = answerSheetMismatchQuadrilaterals
        return result


    def _findAnswerSheetQuadrilaterals(self, frameOrientationMatches, frameAlignmentMatches):
        otherPoints = []
        for frameAlignmentMatch in frameAlignmentMatches:
            otherPoints.append(frameAlignmentMatch.center)

        quadrilaterals = set()
        for frameOrientationMatch in frameOrientationMatches:
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

    def __extractAnswerSheetFrame(self, picture, quadrilateral):
        scaledQuadrilateral = quadrilateral.scaledBy(self.__ANSWER_SHEET_QUADRILATERAL_SCALE)
        if scaledQuadrilateral.isClockwise:
            counterclockwiseScaledQuadrilateral = scaledQuadrilateral.mirrored()
        else:
            counterclockwiseScaledQuadrilateral = scaledQuadrilateral

        projectedAnswerSheetPicture = self.__projectCounterclockwiseQuadrilateralToFrame(picture, counterclockwiseScaledQuadrilateral)

        frame = Frame()
        frame.originalQuadrilateral = quadrilateral
        frame.scaledQuadrilateral = scaledQuadrilateral
        frame.projectedPicture = projectedAnswerSheetPicture
        return frame

    @staticmethod
    def __projectCounterclockwiseQuadrilateralToFrame(picture, counterclockwiseQuadrilateral):
        projectionSize = int(counterclockwiseQuadrilateral.largestSideLength)
        projectionSquare = ConvexQuadrilateral([(projectionSize-1, projectionSize-1), (0, projectionSize-1), (0, 0), (projectionSize-1, 0)])
        return PerspectiveUtil.projectQuadrilateralToSquarePicture(picture, counterclockwiseQuadrilateral, projectionSquare)
import math

from FrameExtractionResult import *
from Frame import *

from ..pattern.FrameAlignmentPatternMatcher import *
from ..pattern.FrameOrientationPatternMatcher import *

from ..geometry.Vector import *
from ..geometry.ConvexQuadrilateral import *
from ..geometry.Square import *
from ..util.MathUtil import *
from ..util.PerspectiveUtil import *

class FrameExtractor:

    def __init__(self, sizeRelaxationRatio=1.10, angleRelaxationInRadians=0.3):
        self._sizeRelaxationRatio = sizeRelaxationRatio
        self._angleRelaxationInRadians = angleRelaxationInRadians
        self._frameAlignmentMatcher = FrameAlignmentPatternMatcher()
        self._frameOrientationMatcher = FrameOrientationPatternMatcher()

    def extractFrames(self, picture):

        frameOrientationMatches = self._frameOrientationMatcher.match(picture, 1)
        frameAlignmentMatches = self._frameAlignmentMatcher.match(picture, 3)

        bestAnswerSheetQuadrilateral = None
        answerSheetQuadrilaterals = self._findAnswerSheetQuadrilaterals(frameOrientationMatches, frameAlignmentMatches)
        if answerSheetQuadrilaterals != []:
            bestAnswerSheetQuadrilateral = self._chooseQuadrilateralThatBestResemblesSquare(answerSheetQuadrilaterals)

        answerSheetFrame = None
        if bestAnswerSheetQuadrilateral != None:
            projectedSquare = bestAnswerSheetQuadrilateral.projectToSquare()
            projectedPicture = PerspectiveUtil.projectQuadrilateralInsidePictureToSquarePicture(picture, bestAnswerSheetQuadrilateral)

            answerSheetFrame = Frame()
            answerSheetFrame.originalQuadrilateral = bestAnswerSheetQuadrilateral
            answerSheetFrame.alignedQuadrilateral = projectedSquare
            answerSheetFrame.alignedPicture = projectedPicture

        result = FrameExtractionResult()
        result.frameOrientationMatches = frameOrientationMatches
        result.frameAlignmentMatches = frameAlignmentMatches
        result.answerSheetFrame = answerSheetFrame

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

    def _chooseQuadrilateralThatBestResemblesSquare(self, frames):
        # TODO
        return frames[0]

    def _findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(self, basePoint, otherPoints):
        convexQuadrilaterals = set()

        for firstPoint in otherPoints:
            baseDistance = self.__getDistance(firstPoint, basePoint)
            for secondPoint in otherPoints:
                if secondPoint == firstPoint:
                    continue                    
                if self.__areDistancesRoughlyEqual(self.__getDistance(firstPoint, secondPoint), baseDistance):
                    for thirdPoint in otherPoints:
                        if thirdPoint == firstPoint or thirdPoint == secondPoint:
                            continue    
                        if self.__areDistancesRoughlyEqual(self.__getDistance(secondPoint, thirdPoint), baseDistance):
                            if self.__areDistancesRoughlyEqual(self.__getDistance(thirdPoint, basePoint), baseDistance):
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

    @staticmethod
    def __getDistance(point1, point2):
        return MathUtil.distanceBetweenPoints(point1, point2)

import numpy as np
import math

from ..pattern.FrameAlignmentPatternMatcher import *
from ..pattern.FrameOrientationPatternMatcher import *

from ..geometry.Vector import *
from ..geometry.ConvexQuadrilateral import *
from ..geometry.Square import *
from ..util.MathUtil import *
from ..util.DrawingUtil import *

class FrameExtractor:

    def __init__(self, sizeRelaxationRatio=1.10, angleRelaxationInRadians=0.3, debugEnabled=True):
        self._sizeRelaxationRatio = sizeRelaxationRatio
        self._angleRelaxationInRadians = angleRelaxationInRadians
        self._debugEnabled = debugEnabled
        self._frameAlignmentMatcher = FrameAlignmentPatternMatcher()
        self._frameOrientationMatcher = FrameOrientationPatternMatcher()


    def extractFrame(self, picture):
        frameOrientationMatches = self._frameOrientationMatcher.match(picture, 1)
        if self._debugEnabled:
            for match in frameOrientationMatches:
                DrawingUtil.drawRectangle(picture, match.location, match.size, DrawingUtil.COLOR_BLUE)

        frameAlignmentMatches = self._frameAlignmentMatcher.match(picture, 3)
        if self._debugEnabled:
            for match in frameAlignmentMatches:
                DrawingUtil.drawRectangle(picture, match.location, match.size, DrawingUtil.COLOR_GREEN)

        possibleFrames = self._findFrames(frameOrientationMatches, frameAlignmentMatches)
        if self._debugEnabled:
            frameOrientationMatchPoints = []
            for match in frameOrientationMatches:
                frameOrientationMatchPoints.append(match.center)
            #print "Frame Orientation Matches: " + str(frameOrientationMatchPoints)
            frameAlignmentMatchPoints = []
            for match in frameAlignmentMatches:
                frameAlignmentMatchPoints.append(match.center)
            #print "Frame Alignment Matches: " + str(frameAlignmentMatchPoints)

            if len(possibleFrames) != 0:
                for frame in possibleFrames:
                    print "Extracted Frame: " + str(frame)
                    DrawingUtil.drawQuadrilateralLines(picture, frame.vertexes, DrawingUtil.COLOR_RED, 1)
                    correctedFrame = Square.projectQuadrilateral(frame)
                    print "Corrected Frame: " + str(correctedFrame)
                    DrawingUtil.drawQuadrilateralLines(picture, correctedFrame.vertexes, DrawingUtil.COLOR_WHITE, 1)
                    DrawingUtil.drawFilledCircle(picture, correctedFrame[0], 3, DrawingUtil.COLOR_YELLOW)
                    for vertex in frame.vertexes:
                        DrawingUtil.drawFilledCircle(picture, vertex, 1, DrawingUtil.COLOR_YELLOW)

        if len(possibleFrames) != 0:
            return possibleFrames[0]
        else:
            return None


    def _findFrames(self, frameOrientationMatches, frameAlignmentMatches):
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

import numpy as np
import math

from FrameAlignmentPatternMatcher import *
from FrameOrientationPatternMatcher import *

from Vector import *
from Quadrilateral import *
from MathUtil import *
from DrawingUtil import *

class FrameExtractor:

    def __init__(self, sizeRelaxationRatio=1.1, angleRelaxationInRadians=0.2, debugEnabled=True):
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

        possibleFrames = self._findPossibleFrames(frameOrientationMatches, frameAlignmentMatches)
        if self._debugEnabled:
            if len(possibleFrames) != 0:
                print "-----"
                for frame in possibleFrames:
                    print "Frame: " + str(frame)
                    DrawingUtil.drawQuadrilateralLines(picture, frame.vertexes, DrawingUtil.COLOR_RED, 1)
                    for vertex in frame.vertexes:
                        DrawingUtil.drawFilledCircle(picture, vertex, 1, DrawingUtil.COLOR_YELLOW)

        if len(possibleFrames) != 0:
            return possibleFrames[0]
        else:
            return None


    def _findPossibleFrames(self, frameOrientationMatches, frameAlignmentMatches):
        otherPoints = []
        for frameAlignmentMatch in frameAlignmentMatches:
            otherPoints.append(frameAlignmentMatch.getCenter())

        quadrilaterals = set()
        for frameOrientationMatch in frameOrientationMatches:
            basePoint = frameOrientationMatch.getCenter()
            quadrilaterals.update(self._findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(basePoint, otherPoints))

        return list(quadrilaterals)


    def _findConvexQuadrilateralsWithRoughlyEqualSizesAndAngles(self, basePoint, otherPoints):
        convexQuadrilaterals = set()

        for firstPoint in otherPoints:
            baseDistance = MathUtil.distanceBetweenPoints(firstPoint, basePoint)
            for secondPoint in otherPoints:
                if secondPoint == firstPoint:
                    continue                    
                if MathUtil.equalWithinRatio(MathUtil.distanceBetweenPoints(firstPoint, secondPoint), baseDistance, self._sizeRelaxationRatio):
                    for thirdPoint in otherPoints:
                        if thirdPoint == firstPoint or thirdPoint == secondPoint:
                            continue    
                        if MathUtil.equalWithinRatio(MathUtil.distanceBetweenPoints(secondPoint, thirdPoint), baseDistance, self._sizeRelaxationRatio):
                            if MathUtil.equalWithinRatio(MathUtil.distanceBetweenPoints(thirdPoint, basePoint), baseDistance, self._sizeRelaxationRatio):
                                quadrilateral = Quadrilateral([basePoint, firstPoint, secondPoint, thirdPoint], self._angleRelaxationInRadians)
                                if quadrilateral.isConvexWithRoughlyRightAngles():
                                    convexQuadrilaterals.add(quadrilateral)
            
        return convexQuadrilaterals
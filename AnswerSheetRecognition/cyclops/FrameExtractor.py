import numpy as np
import math

from FrameAlignmentPatternMatcher import *
from FrameOrientationPatternMatcher import *

from MathUtil import *
from DrawingUtil import *

class FrameExtractor:

    def __init__(self, debugEnabled=True):
        self._frameAlignmentMatcher = FrameAlignmentPatternMatcher()
        self._frameOrientationMatcher = FrameOrientationPatternMatcher()
        self.debugEnabled = debugEnabled

    def extractFrame(self, picture):
        frameOrientationMatches = self._frameOrientationMatcher.match(picture, 1)
        if self.debugEnabled:
            for match in frameOrientationMatches:
                print "Frame Orientation: " + str(match.getCenter())
                DrawingUtil.drawRectangle(picture, match.location, match.size, (0,0,255)) # Blue

        frameAlignmentMatches = self._frameAlignmentMatcher.match(picture, 3)
        if self.debugEnabled:
            for match in frameAlignmentMatches:
                print "Frame Alignment: " + str(match.getCenter())
                DrawingUtil.drawRectangle(picture, match.location, match.size, (0,255,0)) # Green

        frame = self._findFrame(frameOrientationMatches, frameAlignmentMatches)
        if self.debugEnabled:
            if frame != None:
                print "Square: " + str(frame)
                for point in frame:
                    DrawingUtil.drawFilledCircle(picture, point, 3, (255,0,0)) # Red

        return frame


    def _findFrame(self, frameOrientationMatches, frameAlignmentMatches):
        otherPoints = []
        for frameAlignmentMatch in frameAlignmentMatches:
            otherPoints.append(frameAlignmentMatch.getCenter())

        for frameOrientationMatch in frameOrientationMatches:
            basePoint = frameOrientationMatch.getCenter()
            square = self._findSquareInListOfPoints(basePoint, otherPoints, error=15)
            if square != None:
                return square

        return None


    def _findSquareInListOfPoints(self, basePoint, otherPoints, error):
        for firstPoint in otherPoints:
            firstDistance = MathUtil.distanceBetweenPoints(firstPoint, basePoint)

            for secondPoint in otherPoints:
                if secondPoint != firstPoint:
                    secondDistance = MathUtil.distanceBetweenPoints(firstPoint, secondPoint)
                    if MathUtil.equalWithinError(secondDistance, firstDistance, error):

                        for thirdPoint in otherPoints:
                            if thirdPoint != firstPoint and thirdPoint != secondPoint:
                                thirdDistance = MathUtil.distanceBetweenPoints(secondPoint, thirdPoint)
                                if MathUtil.equalWithinError(thirdDistance, firstDistance, error):

                                    fourthDistance = MathUtil.distanceBetweenPoints(thirdPoint, basePoint)
                                    if MathUtil.equalWithinError(fourthDistance, firstDistance, error):
                                        return [basePoint, firstPoint, secondPoint, thirdPoint]
            
        return None

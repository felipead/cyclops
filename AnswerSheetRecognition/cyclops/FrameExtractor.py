from cv2 import rectangle
from cv import RGB

import numpy as np
import math

from FrameAlignmentPatternMatcher import *
from FrameOrientationPatternMatcher import *

from MathUtil import *

class FrameExtractor:

    def __init__(self):
        self._frameAlignmentMatcher = FrameAlignmentPatternMatcher()
        self._frameOrientationMatcher = FrameOrientationPatternMatcher()

    def extractFrame(self, picture):
        frameOrientationMatches = self._frameOrientationMatcher.match(picture, 1)
        # TODO: debug info only
        for match in frameOrientationMatches:
            print "Frame Orientation: " + str(match.location)
            self._drawRectangleInPicture(picture, match.location, match.size, RGB(0,0,255)) # Blue

        frameAlignmentMatches = self._frameAlignmentMatcher.match(picture, 3)
        # TODO: debug info only
        for match in frameAlignmentMatches:
            print "Frame Alignment: " + str(match.location)
            self._drawRectangleInPicture(picture, match.location, match.size, RGB(0,255,0)) # Green

        frame = self._findFrame(frameOrientationMatches, frameAlignmentMatches)
        # TODO: debug info only
        if frame != None:
            print "Square: " + str(frame)
            for point in frame:
                self._drawRectangleInPicture(picture, point, (5,5), RGB(255,0,0)) # Red

        return frame


    def _drawRectangleInPicture(self, picture, location, size, color):
        rectangle(picture, location, (location[0] + size[0], location[1] + size[1]), color, 2)

    def _findFrame(self, frameOrientationMatches, frameAlignmentMatches):
        for frameOrientationMatch in frameOrientationMatches:
            basePoint = frameOrientationMatch.location
            otherPoints = []
            for frameAlignmentMatch in frameAlignmentMatches:
                otherPoints.append(frameAlignmentMatch.location)

            square = self._findSquareInListOfPoints(basePoint, otherPoints, error=20)
            if square != None:
                return square

        return None

    def _findSquareInListOfPoints(self, basePoint, otherPoints, error):
        for firstPoint in otherPoints:
            firstDistance = MathUtil.getDistanceBetween2dPoints(firstPoint, basePoint)

            for secondPoint in otherPoints:
                if secondPoint != firstPoint:
                    secondDistance = MathUtil.getDistanceBetween2dPoints(firstPoint, secondPoint)
                    if MathUtil.isEqualsWithinError(secondDistance, firstDistance, error):

                        for thirdPoint in otherPoints:
                            if thirdPoint != firstPoint and thirdPoint != secondPoint:
                                thirdDistance = MathUtil.getDistanceBetween2dPoints(secondPoint, thirdPoint)
                                if MathUtil.isEqualsWithinError(thirdDistance, secondDistance, error):

                                    fourthDistance = MathUtil.getDistanceBetween2dPoints(thirdPoint, basePoint)
                                    if MathUtil.isEqualsWithinError(fourthDistance, thirdDistance, error):
                                        return [basePoint, firstPoint, secondPoint, thirdPoint]
            
        return None
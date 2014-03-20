# -*- coding: utf-8 -*-

from Vector import *
from ConvexPolygon import *
from ..util.MathUtil import *

import math

"""
A quadrilateral, sometimes also known as a tetragon or quadrangle (Johnson 1929, p. 61) is a 
four-sided polygon. If not explicitly stated, all four polygon vertices are generally taken to lie
in a plane. (If the points do not lie in a plane, the quadrilateral is called a skew quadrilateral.)
There are three topological types of quadrilaterals (Wenninger 1983, p. 50): convex quadrilaterals,
concave quadrilaterals, and crossed quadrilaterals (or butterflies, or bow-ties).
http://mathworld.wolfram.com/Quadrilateral.html
http://en.wikipedia.org/wiki/Quadrilateral
"""
class ConvexQuadrilateral(ConvexPolygon):

    __90_DEGREES = math.pi/2

    def __init__(self, vertexes):
        super(ConvexQuadrilateral, self).__init__(vertexes)
        if len(vertexes) != 4:
            raise Exception("Quadrilateral must have 4 vertexes.")
        
        self._largestSideLength = None
        self._reversedContour = None

        self._bottomLeftCorner = None
        self._topLeftCorner = None
        self._bottomRightCorner = None
        self._topRightCorner = None

    @property
    def largestSideLength(self):
        if self._largestSideLength is None:
            self._largestSideLength = self.__findLargestSideVector().norm
        return self._largestSideLength

    @property
    def bottomLeftCorner(self):
        if self._bottomLeftCorner is None:
            self.__findCorners()
        return self._bottomLeftCorner

    @property
    def bottomRightCorner(self):
        if self._bottomRightCorner is None:
            self.__findCorners()
        return self._bottomRightCorner

    @property
    def topLeftCorner(self):
        if self._topLeftCorner is None:
            self.__findCorners()
        return self._topLeftCorner

    @property
    def topRightCorner(self):
        if self._topRightCorner is None:
            self.__findCorners()
        return self._topRightCorner

    @property
    def reversedContour(self):
        if self._reversedContour == None:
            (a, b, c, d) = self.contour
            self._reversedContour = (reversed(d), reversed(c), reversed(b), reversed(a))
        return self._reversedContour


    def hasRightInteriorAngles(self):
        return self.hasRightInteriorAnglesWithRelaxationOf(0)

    def hasRightInteriorAnglesWithRelaxationOf(self, relaxationInRadians):
        rightAngle = self.__90_DEGREES
        for angle in self.interiorAngles:
            if angle < (rightAngle - relaxationInRadians) or angle > (rightAngle + relaxationInRadians):
                return False
        return True

    def hasEqualSides(self):
        return self.hasEqualSidesWithRelaxationRatioOf(1.0)

    def hasEqualSidesWithRelaxationRatioOf(self, relaxationRatio):
        (size1, size2, size3, size4) = map((lambda v : v.norm), self.contour)
        return MathUtil.equalWithinRatio(size1, size2, relaxationRatio) and MathUtil.equalWithinRatio(size1, size3, relaxationRatio) \
            and MathUtil.equalWithinRatio(size1, size4, relaxationRatio)

    """
    Gets a new quadrilateral rotated clockwise by a certain angle (in radians) along 
    this quadrilateral center.
    This method may suffer from floating point precision loss.
    """
    def clockwiseRotationBy(self, angleInRadians):
        return self.counterclockwiseRotationBy(-angleInRadians)

    """
    Gets a new quadrilateral rotated counterclockwise by a certain angle (in radians)
    along this quadrilateral center.
    This method may suffer from floating point precision loss.
    """
    def counterclockwiseRotationBy(self, angleInRadians):
        cos = math.cos(angleInRadians)
        sin = math.sin(angleInRadians)
        center = self.centroid

        rotatedVertexes = []
        for v in self.vertexes:
            rotatedX = (v.x - center.x) * cos  -  (v.y - center.y) * sin + center.x;
            rotatedY = (v.x - center.x) * sin  +  (v.y - center.y) * cos + center.y;
            rotatedPoint = Point((rotatedX, rotatedY))
            rotatedVertexes.append(rotatedPoint)
        return ConvexQuadrilateral(rotatedVertexes)

    """
    Gets a new quadrilateral rotated 90˚ clockwise along this quadrilateral center.
    This method does not suffer from floating point precision loss.
    """
    def clockwiseRotationBy90Degrees(self):
        center = self.centroid
        rotatedVertexes = []
        for v in self.vertexes:
            rotatedX =   (v.y - center.y) + center.x;
            rotatedY = - (v.x - center.x) + center.y;
            rotatedPoint = Point((rotatedX, rotatedY))
            rotatedVertexes.append(rotatedPoint)
        return ConvexQuadrilateral(rotatedVertexes)

    """
    Gets a new quadrilateral rotated 90˚ counterclockwise along this quadrilateral center.
    This method does not suffer from floating point precision loss.
    """
    def counterclockwiseRotationBy90Degrees(self):
        center = self.centroid
        rotatedVertexes = []
        for v in self.vertexes:
            rotatedX = - (v.y - center.y) + center.x;
            rotatedY =   (v.x - center.x) + center.y;
            rotatedPoint = Point((rotatedX, rotatedY))
            rotatedVertexes.append(rotatedPoint)
        return ConvexQuadrilateral(rotatedVertexes)

    """
    Project this quadrilateral to a square with sides equal to the largest side of this polygon.
    Useful for perspective correction.
    
    If this quadrilateral is a lozenge or trapezoid representing a deformed square (for instance,
    a square seen from a angular perspective), then the output of this method will be an approximated 
    square that best represents the original square.

    If this quadrilateral is a rectangle or another shape not representing a square, then
    the resulting projection will be a deformed rectangle or shape projected over a square, respectively.
    """
    def projectToSquare(self):
        vectorAB = self.__findLargestSideVector()
        vectorBA = vectorAB.reflection()

        vectorAD = None
        vectorBC = None
        if self.isClockwise:
            vectorAD = vectorAB.clockwiseRotationBy90Degrees()
            vectorBC = vectorBA.counterclockwiseRotationBy90Degrees()
        else:
            vectorAD = vectorAB.counterclockwiseRotationBy90Degrees()
            vectorBC = vectorBA.clockwiseRotationBy90Degrees()

        indexA = self.vertexes.index(vectorAB.tail)
        indexB = self.vertexes.index(vectorAB.head)
        indexC = (indexB + 1) % 4
        indexD = (indexA - 1) % 4

        correctedVertexes = list(self.vertexes)
        correctedVertexes[indexC] = vectorBC.head
        correctedVertexes[indexD] = vectorAD.head

        square = ConvexQuadrilateral(correctedVertexes)
        return square

    def __findLargestSideVector(self):
        largestSide = None
        largestSideLength = 0

        for side in self.contour:
            sideLength = side.norm
            if sideLength > largestSideLength:
                largestSide = side
                largestSideLength = sideLength

        return largestSide


    # FIXME: remove tuple, fix Point hashCode and equals
    def __findCorners(self):
        projectedSquare = self.projectToSquare()
        projectedSquareSortedVertexes = self.__sortVertexesOfSquareCounterclockwiseWithBottomLeftVertexFirst(projectedSquare)

        thisQuadrilateralVertexSet = set([tuple(v) for v in self.vertexes])
        projectedSquareVertexSet = set(projectedSquareSortedVertexes)
        vertexesInBothThisQuadrilateralAndItsProjectedSquare = (thisQuadrilateralVertexSet & projectedSquareVertexSet)
        vertexesNotInTheProjectedSquare = list(thisQuadrilateralVertexSet - projectedSquareVertexSet)

        thisQuadrilateralSortedVertexes = [None, None, None, None]
        missingIndexes = []
        for index in xrange(len(projectedSquareSortedVertexes)):
            vertex = projectedSquareSortedVertexes[index]
            if vertex in vertexesInBothThisQuadrilateralAndItsProjectedSquare:
                thisQuadrilateralSortedVertexes[index] = vertex
            else:
                missingIndexes.append(index)

        if len(missingIndexes) == 1:
            thisQuadrilateralSortedVertexes[missingIndexes[0]] = vertexesNotInTheProjectedSquare[0]
        elif len(missingIndexes) == 2:
            thisQuadrilateralSortedVertexes[missingIndexes[0]] = vertexesNotInTheProjectedSquare[0]
            thisQuadrilateralSortedVertexes[missingIndexes[1]] = vertexesNotInTheProjectedSquare[1]

        self._bottomLeftCorner = thisQuadrilateralSortedVertexes[0]
        self._bottomRightCorner = thisQuadrilateralSortedVertexes[1]
        self._topRightCorner = thisQuadrilateralSortedVertexes[2]
        self._topLeftCorner = thisQuadrilateralSortedVertexes[3]


    # FIXME: remove tuple, fix Point hashCode and equals
    @staticmethod
    def __sortVertexesOfSquareCounterclockwiseWithBottomLeftVertexFirst(square):
        topLine = []
        bottomLine = []
        middle = []
        centerY = square.centroid.y

        for vertex in square.vertexes:
            if vertex.y > centerY:
                topLine.append(vertex)
            elif vertex.y < centerY:
                bottomLine.append(vertex)
            else: # equal
                middle.append(vertex)

        if len(middle) == 2:
            if middle[0].x < middle[1].x:
                topLine.append(middle[0])
                bottomLine.append(middle[1])
            else:
                bottomLine.append(middle[0])
                topLine.append(middle[1])

        if topLine[0].x < topLine[1].x:
            topLeft = topLine[0]
            topRight = topLine[1]
        else:
            topLeft = topLine[1]
            topRight = topLine[0]

        if bottomLine[0].x < bottomLine[1].x:
            bottomLeft = bottomLine[0]
            bottomRight = bottomLine[1]
        else:
            bottomLeft = bottomLine[1]
            bottomRight = bottomLine[0]

        return (tuple(bottomLeft), tuple(bottomRight), tuple(topRight), tuple(topLeft))
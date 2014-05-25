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
        self._shortestSideLength = None
        self._reversedContour = None
        self._mirroredVertexes = None

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
    def shortestSideLength(self):
        if self._shortestSideLength is None:
            self._shortestSideLength = self.__findShortestSideVector().norm
        return self._shortestSideLength

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
    def mirroredVertexes(self):
        if self._mirroredVertexes == None:
            self._mirroredVertexes = (self._vertexes[0], self._vertexes[3], self._vertexes[2], self._vertexes[1])
        return self._mirroredVertexes

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

    def asClockwise(self):
        if self.isClockwise:
            return self
        else:
            return self.mirrored()

    def asCounterclockwise(self):
        if self.isClockwise:
            return self.mirrored()
        else:
            return self

    def mirrored(self):
        return ConvexQuadrilateral(self.mirroredVertexes)

    """
    Scale this quadrilateral uniformly by a percentage factor. Factor is such that:
        1 is 100%
        2 is 200%
        0.5 is 50%
        ...
    """
    def scaledBy(self, scaleFactor):
        if scaleFactor <= 0:
            raise Exception("Scale factor must be greater than zero.")
        center = self.centroid
        newVertexes = []
        for vertex in self.vertexes:
            scaled = Vector(vertex, center).multipliedByScalar(scaleFactor)
            newVertexes.append(scaled.head)
        return ConvexQuadrilateral(newVertexes)

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

    def __findShortestSideVector(self):
        shortestSide = None
        shortestSideLength = float("inf")

        for side in self.contour:
            sideLength = side.norm
            if sideLength < shortestSideLength:
                shortestSide = side
                shortestSideLength = sideLength

        return shortestSide

    def __findCorners(self):
        top = []
        bottom = []
        middle = []
        center = self.centroid

        # First we collect the points which are higher, lower and on the same level than the
        #  centroid (y coordinates).
        for vertex in self.vertexes:
            if vertex.y > center.y:
                top.append(vertex)
            elif vertex.y < center.y:
                bottom.append(vertex)
            else: 
                middle.append(vertex)

        # If we have middle points then two vertexes and the centroid are connected by
        # a line parallel to the x axis. This happens, for instance, if this quadrilateral
        # is a perfect square rotated exactly 45˚ around the x axis.
        if len(middle) == 2:
            if middle[0].x < middle[1].x:
                top.append(middle[0])
                bottom.append(middle[1])
            else:
                bottom.append(middle[0])
                top.append(middle[1])

        # If this quadrilateral has a vertex that is too far from the others (for instance, a 
        # unbalaced trapezoid), then its centroid will be near that vertex. When that happens,
        # the remaining 3 vertexes are so distant from the centroid that we might capture
        # more than two bottom or top points. Here we fix this, moving a possible extra bottom
        # point to the list of top points, and vice versa.
        if len(bottom) == 3:
            p = self.__findPointWithBiggestY(bottom)
            bottom.remove(p)
            top.append(p)
        elif len(top) == 3:
            p = self.__findPointWithSmallestY(top)
            top.remove(p)
            bottom.append(p)

        # Now that we have determined the top and bottom points, determine which ones
        # belong to the left and which ones belong to the right.
        if top[0].x < top[1].x:
            self._topLeftCorner = top[0]
            self._topRightCorner = top[1]
        else:
            self._topLeftCorner = top[1]
            self._topRightCorner = top[0]
        if bottom[0].x < bottom[1].x:
            self._bottomLeftCorner = bottom[0]
            self._bottomRightCorner = bottom[1]
        else:
            self._bottomLeftCorner = bottom[1]
            self._bottomRightCorner = bottom[0]

    @staticmethod
    def __findPointWithBiggestY(points):
        pointWithBiggestY = points[0]
        for point in points[1:]:
            if point.y > pointWithBiggestY.y:
                pointWithBiggestY = point
        return pointWithBiggestY

    @staticmethod
    def __findPointWithSmallestY(points):
        pointWithSmallestY = points[0]
        for point in points[1:]:
            if point.y < pointWithSmallestY.y:
                pointWithSmallestY = point
        return pointWithSmallestY

    def __repr__(self):
        return "ConvexQuadrilateral" + repr(self._vertexes)
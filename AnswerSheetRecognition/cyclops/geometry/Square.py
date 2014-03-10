# -*- coding: utf-8 -*-

from ConvexQuadrilateral import *

"""
Square is a geometric figure consisting of a convex quadrilateral with sides of equal length that
are positioned at right angles to each other. In other words, a square is a regular polygon with
four sides.
http://mathworld.wolfram.com/Square.html
"""
class Square(ConvexQuadrilateral):
    
    def __init__(self, vertexes):
        super(Square,self).__init__(vertexes)
        if not self.hasRightInteriorAngles():
            raise Exception("All square angles must be 90 degrees.")
        if not self.hasEqualSides():
            raise Exception("All square sides must be equal.")
        self._sideLength = None

    @property
    def sideLength(self):
        if self._sideLength == None:
            self._sideLength = Vector(self[0], self[1]).norm
        return self._sideLength


    """
    Project a quadrilateral to a square with sides equal to the largest side of this polygon.
    Useful for perspective correction.
    
    If the quadrilateral is a lozenge or trapezoid representing a deformed square (for instance,
    a square seen from a angular perspective), then the output of this method will be a square that best
    represents the original square.

    If the quadrilateral is a rectangle or another shape not representing a square, then
    the resulting projection will be a deformed rectangle or shape projected over a square, respectively.
    """
    @classmethod
    def projectQuadrilateral(class_, quadrilateral):
        if len(quadrilateral) != 4:
            raise Exception("Only quadrilaterals are supported.")

        vectorAB = Square.__findLargestSideVector(quadrilateral.contour)
        vectorBA = vectorAB.reflection()

        vectorAD = None
        vectorBC = None
        if quadrilateral.isClockwise:
            vectorAD = vectorAB.clockwiseRotationBy90Degrees()
            vectorBC = vectorBA.counterclockwiseRotationBy90Degrees()
        else:
            vectorAD = vectorAB.counterclockwiseRotationBy90Degrees()
            vectorBC = vectorBA.clockwiseRotationBy90Degrees()

        indexA = quadrilateral.vertexes.index(vectorAB.tail)
        indexB = quadrilateral.vertexes.index(vectorAB.head)
        indexC = (indexB + 1) % 4
        indexD = (indexA - 1) % 4

        correctedVertexes = list(quadrilateral.vertexes)
        correctedVertexes[indexC] = vectorBC.head
        correctedVertexes[indexD] = vectorAD.head

        square = Square(correctedVertexes)
        return square

    @staticmethod
    def __findLargestSideVector(contour):
        largestSide = None
        largestSideLength = 0

        for side in contour:
            sideLength = side.norm
            if sideLength > largestSideLength:
                largestSide = side
                largestSideLength = sideLength

        return largestSide
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
"""
class ConvexQuadrilateral(ConvexPolygon):

    def __init__(self, vertexes):
        super(ConvexQuadrilateral, self).__init__(vertexes)
        if len(vertexes) != 4:
            raise Exception("Quadrilateral must have 4 vertexes.")

    def hasRightInteriorAngles(self):
        return self.hasRightInteriorAnglesWithRelaxationOf(0)

    def hasRightInteriorAnglesWithRelaxationOf(self, relaxationInRadians):
        rightAngle = Angles._90_DEGREES
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
            
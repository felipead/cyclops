import unittest
from unittest import TestCase

import math

from ..MathUtil import *
from ..Vector import *

class VectorTest(TestCase):

    def testCreate2DimensionVectorInstanceWithoutOrigin(self):
        (x, y) = (1, 2)
        v = Vector((x,y))
        assert len(v) == 2
        assert v[0] == x
        assert v[1] == y

    def testCreate2DimensionVectorInstanceWithOrigin(self):
        (x0, y0) = (1, 2)
        (x1, y1) = (5, -6)
        v = Vector.create((x1,y1), (x0,y0))
        assert len(v) == 2
        assert v[0] == x1 - x0
        assert v[1] == y1 - y0

    def testCalculateInnerProductBetween2DimensionVectors(self):
        (v1,v2) = (3,4)
        v = Vector((v1,v2))

        (w1,w2) = (3,4)
        w = Vector((w1,w2))
        assert v.innerProduct(w) == v1*w1 + v2*w2

    def testCalculateNormOf2DimensionVector(self):
        (v1,v2) = (3,4)
        v = Vector((v1,v2))

        assert v.norm() == math.sqrt(v1*v1 + v2*v2)


    def testCalculateAngleBetween2DimensionVectorsWith0Degrees(self):
        error=0.0000001
        v = Vector((7,14.6))
        w = Vector((3.5,7.3))

        assert v.innerProduct(w) > 0

        angle = v.angleBetween(w)
        assert MathUtil.equalWithinError(angle, 0, error)

    def testCalculateAngleBetween2DimensionVectorsWith45Degrees(self):
        error=0.00000000001
        v = Vector((6,0))
        w = Vector((3,3))

        assert v.innerProduct(w) > 0

        angle = v.angleBetween(w)
        assert MathUtil.equalWithinError(angle, (math.pi/4), error)

    def testCalculateAngleBetween2DimensionVectorsWith90Degrees(self):
        error=0.00000000001
        v = Vector((0,5))
        w = Vector((14.293,0))

        assert MathUtil.equalWithinError(v.innerProduct(w), 0, error)

        angle = v.angleBetween(w)
        assert MathUtil.equalWithinError(angle, math.pi/2, error)


    def testCalculateAngleBetween2DimensionVectorsWithLessThan90Degrees(self):
        v = Vector((4,5))
        w = Vector((1,2))

        assert v.innerProduct(w) > 0

        angle = v.angleBetween(w)
        assert angle < (math.pi/2)

    def testCalculateAngleBetween2DimensionVectorsWithMoreThan90Degrees(self):
        v = Vector((-6,2))
        w = Vector((5,1))

        assert v.innerProduct(w) < 0

        angle = v.angleBetween(w)
        assert angle > (math.pi/2)

    def testCalculateAngleBetween2DimensionVectorsWith180Degrees(self):
        error=0.0000001
        v = Vector((-7,-14.6))
        w = Vector((3.5,7.3))

        assert v.innerProduct(w) < 0

        angle = v.angleBetween(w)
        assert MathUtil.equalWithinError(angle, math.pi, error)

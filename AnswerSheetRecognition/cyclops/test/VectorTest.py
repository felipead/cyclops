import unittest
from unittest import TestCase

import math

from ..util.MathUtil import *
from ..geometry.Vector import *

class VectorTest(TestCase):

    def testCreateVectorInstanceWithTerminalPoint(self):
        (x, y) = (1, 2)
        v = Vector((x,y))
        assert len(v) == 2
        assert v.x == x
        assert v.y == y

    def testCreateVectorInstanceWithTerminalAndInitialPoints(self):
        (x0, y0) = (1, 2)
        (x1, y1) = (5, -6)
        v = Vector((x1,y1), (x0,y0))
        assert len(v) == 2
        assert v.x == x1 - x0
        assert v.y == y1 - y0

    def testAccessVectorCoordinates(self):
        (x, y) = (9, 5)
        v = Vector((x,y))
        assert v[0] == v.x == v.coordinates[0] == x
        assert v[1] == v.y == v.coordinates[1] == y

    def testLengthOfVectorIsAlwaysTwoBecauseOnly2DimensionVectorsAreSupported(self):
        v = Vector((5,3))
        assert len(v) == 2

    def testVectorIsNotEqualToObjectWithOtherType(self):
        assert Vector((5,5)) != (5,5)

    def testVectorsWithSameCoordinatesAreEqual(self):
        p = (3,2)
        assert Vector(p) == Vector(p)

    def testVectorsWithDifferentCoordinatesAreDifferent(self):
        assert Vector((5,3)) != Vector((3,5))

    def testHashCodeShouldDependOnlyOnCoordinates(self):
        assert hash(Vector((5,5))) != hash(Vector((5,5.1)))


    def testInnerProductBetweenVectors(self):
        (v1,v2) = (3,4.23)
        v = Vector((v1,v2))

        (w1,w2) = (8.65,3.5)
        w = Vector((w1,w2))
        assert v.innerProduct(w) == v1*w1 + v2*w2

    def testInnerProductBetweenVectorAndZeroIsZero(self):
        vector = Vector((5,5))
        zero = Vector((0,0))

        assert vector.angleBetween(zero) == 0
        assert zero.angleBetween(vector) == 0


    def testNorm(self):
        (v1,v2) = (3,4)
        v = Vector((v1,v2))

        assert v.norm() == math.sqrt(v1*v1 + v2*v2)


    def testAngleBetweenVectorAndZeroIsZero(self):
        zero = Vector((0,0))
        vector = Vector((5,-31))

        assert zero.angleBetween(vector) == 0
        assert vector.angleBetween(zero) == 0

    def testAngleBetweenZeroAndZeroIsZero(self):
        zero = Vector((0,0))
        assert zero.angleBetween(zero) == 0

    def testAngleBetweenEqualVectorsIsZero(self):
        v = Vector((-63, 326))
        w = Vector(v.coordinates)

        assert v.angleBetween(w) == 0
        assert w.angleBetween(v) == 0

    def testAngleBetweenOppositeVectorsIs180Degrees(self):
        error=0.0000001
        v = Vector((5, 5))
        w = Vector((-5, -5))

        assert v.innerProduct(w) < 0

        expectedAngle = math.pi
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenParallelVectorsIsZero(self):
        error=0.0000001
        v = Vector((7,14.6))
        w = Vector((3.5,7.3))

        assert v.innerProduct(w) > 0

        expectedAngle = 0
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIs45Degrees(self):
        error=0.00000000001
        v = Vector((6,0))
        w = Vector((3,3))

        assert v.innerProduct(w) > 0

        expectedAngle = math.pi/4
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIs90Degrees(self):
        error=0.00000000001
        v = Vector((0,5))
        w = Vector((14.293,0))

        assert MathUtil.equalWithinError(v.innerProduct(w), 0, error)

        expectedAngle = math.pi/2
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIsLessThan90Degrees(self):
        v = Vector((4,5))
        w = Vector((1,2))

        assert v.innerProduct(w) > 0

        maximumAngle = math.pi/2
        assert v.angleBetween(w) < maximumAngle
        assert w.angleBetween(v) < maximumAngle

    def testAngleBetweenVectorsIsMoreThan90Degrees(self):
        v = Vector((-6,2))
        w = Vector((5,1))

        assert v.innerProduct(w) < 0

        minimumAngle = (math.pi/2)
        assert v.angleBetween(w) > minimumAngle
        assert w.angleBetween(v) > minimumAngle

    def testAngleBetweenVectorsIs180Degrees(self):
        error=0.0000001
        v = Vector((-7,-14.6))
        w = Vector((3.5,7.3))

        assert v.innerProduct(w) < 0

        expectedAngle = math.pi
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)
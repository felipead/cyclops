import unittest
from unittest import TestCase

import math

from ..util.MathUtil import *
from ..geometry.Vector import *

class VectorTest(TestCase):

    def testCreate2dVectorInstanceWithTerminalPointAsTuple(self):
        (x, y) = (1, 2)
        v = Vector((x,y))
        assert v.x == x
        assert v.y == y
        assert v.z == 0

    def testCreate2dVectorInstanceWithTerminalAndInitialPointsAsTuples(self):
        (x0, y0) = (1, 2)
        (x1, y1) = (5, -6)
        v = Vector((x1,y1), (x0,y0))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == 0

    def testCreate2dVectorInstanceWithTerminalAndInitialPointsAsVectors(self):
        (x0, y0) = (1, 2)
        (x1, y1) = (5, -6)
        v = Vector(Vector((x1,y1)), Vector((x0,y0)))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == 0

    def testCreate3dVectorInstanceWithTerminalPointAsTuple(self):
        (x, y, z) = (1, 2, 3)
        v = Vector((x,y,z))
        assert v.x == x
        assert v.y == y
        assert v.z == z

    def testCreate3dVectorInstanceWithTerminalAndInitialPointsAsTuples(self):
        (x0, y0, z0) = (1, 2, 7)
        (x1, y1, z1) = (5, -6, -4)
        v = Vector((x1,y1,z1), (x0,y0,z0))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == z1 - z0

    def testCreate3dVectorInstanceWithTerminalAndInitialPointsAsVectors(self):
        (x0, y0, z0) = (1, 2, -3)
        (x1, y1, z1) = (5, -6, 9)
        v = Vector(Vector((x1,y1,z1)), Vector((x0,y0,z0)))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == z1 - z0

    def testCanNotCreateVectorsWithMoreThan3Dimensions(self):
        exceptionThrown = False
        try:
            Vector((1,2,3,4))
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown

    def testCanNotCreateVectorsWithLessThan2Dimensions(self):
        exceptionThrown = False
        try:
            Vector((1,))
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown


    def testAccess2dVectorCoordinates(self):
        (x, y) = (9, 5)
        v = Vector((x,y))
        assert v[0] == v.x == v.coordinates[0] == x
        assert v[1] == v.y == v.coordinates[1] == y
        assert v[2] == v.z == v.coordinates[2] == 0

    def testAccess3dVectorCoordinates(self):
        (x, y, z) = (9, 5, 8)
        v = Vector((x,y,z))
        assert v[0] == v.x == v.coordinates[0] == x
        assert v[1] == v.y == v.coordinates[1] == y
        assert v[2] == v.z == v.coordinates[2] == z

    def test2dAnd3dVectorsHaveLength3(self):
        v1 = Vector((5,3))
        assert len(v1) == len(v1.coordinates) == 3

        v2 = Vector((5,3,8))
        assert len(v2) == len(v2.coordinates) == 3


    def testVectorIsNotEqualToObjectWithDifferentType(self):
        assert Vector((5,5)) != (5,5)
        assert Vector((5,5)) != 5

    def testVectorsWithSameCoordinatesAreEqual(self):
        (x,y,z) = (3,2,10)

        assert Vector((x,y)) == Vector((x,y)) == Vector((x,y,0))
        assert Vector((x,y,z)) == Vector((x,y,z))

    def testVectorsWithDifferentCoordinatesAreDifferent(self):
        assert Vector((5,3)) != Vector((3,5))
        assert Vector((5,3)) != Vector((5,3,9))

    def testHashCodeShouldBeAFunctionOfTheCoordinates(self):
        assert hash(Vector((5,5))) != hash(Vector((5,5.1)))
        assert hash(Vector((7,8))) != hash(Vector((7,8,9)))
        assert hash(Vector((7,8,9))) == hash(Vector((7,8,9)))

    def testToString(self):
        assert str(Vector((3,2,5))) == str((3,2,5))
        assert str(Vector((3,2))) == str((3,2,0))

    def testIterable(self):
        (x,y,z) = (3,5,7)
        sum = 0
        for i in Vector((x,y,z)):
            sum += i
        assert sum == x + y + z


    def testDotProductBetween2dVectors(self):
        (v1,v2) = (3,4.23)
        v = Vector((v1,v2))
        (w1,w2) = (8.65,3.5)
        w = Vector((w1,w2))

        assert v.dotProduct(w) == v1*w1 + v2*w2

    def testDotProductBetween3dVectors(self):
        (v1,v2,v3) = (3,4.23,8)
        v = Vector((v1,v2,v3))
        (w1,w2,w3) = (8.65,3.5,13.9)
        w = Vector((w1,w2,w3))

        assert v.dotProduct(w) == v1*w1 + v2*w2 + v3*w3

    def testDotProductBetween2dAnd3dVectors(self):
        (v1,v2) = (3,4.23)
        v = Vector((v1,v2))

        (w1,w2,w3) = (8.65,3.5,13.9)
        w = Vector((w1,w2,w3))

        assert v.dotProduct(w) == v1*w1 + v2*w2

    def testDotProductBetweenVectorAndZeroIsZero(self):
        vector = Vector((5,5,7))
        zero = Vector((0,0))

        assert vector.angleBetween(zero) == 0
        assert zero.angleBetween(vector) == 0

    def testClockwiseCrossProductBetweenTwo2dVectors90DegreesAwayHasNegativeZ(self):
        v1 = Vector((0,50))
        v2 = Vector((100,0))
        clockwise = v1.crossProduct(v2)
        assert clockwise[0] == 0
        assert clockwise[1] == 0
        assert clockwise[2] == -clockwise.norm() == - (v1.norm() * v2.norm()) < 0

    def testCounterClockwiseCrossProductBetweenTwo2dVectors90DegreesAwayHasPositiveZ(self):
        v1 = Vector((0,50))
        v2 = Vector((100,0))
        counterclockwise = v2.crossProduct(v1)
        assert counterclockwise[0] == 0
        assert counterclockwise[1] == 0
        assert counterclockwise[2] == counterclockwise.norm() == (v1.norm() * v2.norm()) > 0

    def testProductBetweenCanonicalBasis(self):
        i = Vector((1,0,0))
        j = Vector((0,1,0))
        k = Vector((0,0,1))

        assert i.crossProduct(j) == Vector((0,0,1))
        assert j.crossProduct(i) == Vector((0,0,-1))

        assert k.crossProduct(i) == Vector((0,1,0))
        assert i.crossProduct(k) == Vector((0,-1,0))

        assert k.crossProduct(j) == Vector((-1,0,0))
        assert j.crossProduct(k) == Vector((1,0,0))

    def testCrossProductBetweenParallelVectorsIsZero(self):
        (x,y,z) = (100,50,5)
        v1 = Vector((x,y,z))
        v2 = Vector((x*2,y*2,z*2))
        assert v1.crossProduct(v2) == Vector((0,0,0))
        assert v2.crossProduct(v1) == Vector((0,0,0))

    def testCrossProductBetweenVectorAndItsReflectionIsZero(self):
        v = Vector((100,50,5))
        reflection = v.reflection()
        assert v.crossProduct(reflection) == Vector((0,0,0))
        assert reflection.crossProduct(v) == Vector((0,0,0))

    def testNormOf2dVector(self):
        (v1,v2) = (3,4)
        v = Vector((v1,v2))
        assert v.norm() == math.sqrt(v1*v1 + v2*v2)

    def testNormOf3dVector(self):
        (v1,v2,v3) = (3,4,5)
        v = Vector((v1,v2,v3))
        assert v.norm() == math.sqrt(v1*v1 + v2*v2 + v3*v3)


    def testAngleBetweenVectorAndZeroIsZero(self):
        zero = Vector((0,0))
        vector = Vector((5,-31,3))

        assert zero.angleBetween(vector) == 0
        assert vector.angleBetween(zero) == 0

    def testAngleBetweenZeroAndZeroIsZero(self):
        zero = Vector((0,0))
        assert zero.angleBetween(zero) == 0

    def testAngleBetweenEqualVectorsIsZero(self):
        error=0.01
        v = Vector((-63,326,5))
        w = Vector(v.coordinates)

        assert MathUtil.equalWithinError(v.angleBetween(w), 0, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), 0, error)

    def testAngleBetweenOppositeVectorsIs180Degrees(self):
        error=0.0000001
        v = Vector((5, 5))
        w = Vector((-5, -5))

        assert v.dotProduct(w) < 0

        expectedAngle = math.pi
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenParallelVectorsIsZero(self):
        error=0.0000001
        v = Vector((7,14.6))
        w = Vector((3.5,7.3))

        assert v.dotProduct(w) > 0

        expectedAngle = 0
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIs45Degrees(self):
        error=0.00000000001
        v = Vector((6,0))
        w = Vector((3,3))

        assert v.dotProduct(w) > 0

        expectedAngle = math.pi/4
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIs90Degrees(self):
        error=0.00000000001
        v = Vector((0,5))
        w = Vector((14.293,0))

        assert MathUtil.equalWithinError(v.dotProduct(w), 0, error)

        expectedAngle = math.pi/2
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIs90Degrees(self):
        error=0.00000000001
        v = Vector((0,5))
        w = Vector((14.293,0))

        assert MathUtil.equalWithinError(v.dotProduct(w), 0, error)

        expectedAngle = math.pi/2
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIsLessThan90Degrees(self):
        v = Vector((4,5))
        w = Vector((1,2))

        assert v.dotProduct(w) > 0

        maximumAngle = math.pi/2
        assert v.angleBetween(w) < maximumAngle
        assert w.angleBetween(v) < maximumAngle

    def testAngleBetweenVectorsIsLessThan90Degrees(self):
        v = Vector((4,5,9))
        w = Vector((1,2,9))

        assert v.dotProduct(w) > 0

        maximumAngle = math.pi/2
        assert v.angleBetween(w) < maximumAngle
        assert w.angleBetween(v) < maximumAngle

    def testAngleBetweenVectorsIsMoreThan90Degrees(self):
        v = Vector((-6,2))
        w = Vector((5,1))

        assert v.dotProduct(w) < 0

        minimumAngle = (math.pi/2)
        assert v.angleBetween(w) > minimumAngle
        assert w.angleBetween(v) > minimumAngle

    def testAngleBetweenVectorsIsMoreThan90Degrees(self):
        v = Vector((-6,2))
        w = Vector((5,1))

        assert v.dotProduct(w) < 0

        minimumAngle = (math.pi/2)
        assert v.angleBetween(w) > minimumAngle
        assert w.angleBetween(v) > minimumAngle

    def testAngleBetweenVectorsIs180Degrees(self):
        error=0.0000001
        v = Vector((-7,-14.6))
        w = Vector((3.5,7.3))

        assert v.dotProduct(w) < 0

        expectedAngle = math.pi
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testAngleBetweenVectorsIs180Degrees(self):
        error=0.001
        v = Vector((-7,-14.6))
        w = Vector((3.5,7.3))

        assert v.dotProduct(w) < 0

        expectedAngle = math.pi
        assert MathUtil.equalWithinError(v.angleBetween(w), expectedAngle, error)
        assert MathUtil.equalWithinError(w.angleBetween(v), expectedAngle, error)

    def testReflection(self):
        v = Vector((3,2,-3), (4,5,1))
        mirror = v.reflection()
        assert mirror.initialPoint == v.terminalPoint
        assert mirror.terminalPoint == v.initialPoint
        assert v.norm() == mirror.norm()
        assert MathUtil.equalWithinError(v.angleBetween(mirror), math.pi, 0.0000001)

    def testReflectionFromReflectionIsTheOriginalVector(self):
        v = Vector((436,-13,40), (-950,30,2.35))
        mirror = v.reflection()
        assert mirror.reflection() == v


    def test90DegreeClockwiseRotationOf2dVector(self):
        v = Vector((3,2), (-1,-50))
        clockwise = v.clockwiseRotationBy90Degrees()
        assert clockwise.dotProduct(v) == 0
        assert clockwise.angleBetween(v) == math.pi/2
        assert clockwise.norm() == v.norm()

    def test90DegreeClockwiseRotationIsClockwiseInComputerGraphicsCoordinatesFor2dVector(self):
        a = 4
        v = Vector((a, 0))
        assert v.clockwiseRotationBy90Degrees() == Vector((0,a))
        assert v.clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees() == Vector((-a,0))
        assert v.clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees() == Vector((0,-a))
        assert v.clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees() == v

    def test90DegreeClockwiseRotationOverCounterClockwiseRotationIsTheOriginal2dVector(self):
        v = Vector((312,460), (-93,517))
        counterclockwise = v.counterClockwiseRotationBy90Degrees()
        assert counterclockwise.clockwiseRotationBy90Degrees() == v


    def test90DegreeCounterClockwiseRotationFor2dVector(self):
        v = Vector((3,2), (-1,-50))
        counterclockwise = v.counterClockwiseRotationBy90Degrees()
        assert counterclockwise.dotProduct(v) == 0
        assert counterclockwise.angleBetween(v) == math.pi/2
        assert counterclockwise.norm() == v.norm()

    def test90DegreeCounterClockwiseRotationIsCounterClockwiseInComputerGraphicsCoordinatesFor2dVector(self):
        a = 4
        v = Vector((a, 0))
        assert v.counterClockwiseRotationBy90Degrees() == Vector((0,-a))
        assert v.counterClockwiseRotationBy90Degrees().counterClockwiseRotationBy90Degrees() == Vector((-a,0))
        assert v.counterClockwiseRotationBy90Degrees().counterClockwiseRotationBy90Degrees().counterClockwiseRotationBy90Degrees() == Vector((0,a))
        assert v.counterClockwiseRotationBy90Degrees().counterClockwiseRotationBy90Degrees().counterClockwiseRotationBy90Degrees().counterClockwiseRotationBy90Degrees() == v

    def test90DegreeCounterClockwiseRotationOverClockwiseRotationIsTheOriginal2dVector(self):
        v = Vector((312,460), (-93,517))
        clockwise = v.clockwiseRotationBy90Degrees()
        assert clockwise.counterClockwiseRotationBy90Degrees() == v

    def test90DegreeClockwiseRotationIsNotImplementedFor3dVectors(self):
        v = Vector((5,7,9))
        exceptionThrown = False
        try:
            v.clockwiseRotationBy90Degrees()
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown

    def test90DegreeCounterClockwiseRotationIsNotImplementedFor2dVectors(self):
        v = Vector((5,7,9))
        exceptionThrown = False
        try:
            v.counterClockwiseRotationBy90Degrees()
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown
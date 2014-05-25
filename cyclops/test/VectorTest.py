import unittest
from unittest import TestCase

import math

from ..util.MathUtil import *
from ..geometry.Vector import *

class VectorTest(TestCase):

    def testCreate2dVectorInstanceWithHeadPointAsTuple(self):
        (x, y) = (1, 2)
        v = Vector((x,y))
        assert v.x == x
        assert v.y == y
        assert v.z == 0

    def testCreate2dVectorInstanceWithHeadAndTailPointsAsTuples(self):
        (x0, y0) = (1, 2)
        (x1, y1) = (5, -6)
        v = Vector((x1,y1), (x0,y0))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == 0

    def testCreate2dVectorInstanceWithHeadAndTailPointsAsVectors(self):
        (x0, y0) = (1, 2)
        (x1, y1) = (5, -6)
        v = Vector(Vector((x1,y1)), Vector((x0,y0)))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == 0

    def testCreate3dVectorInstanceWithHeadPointAsTuple(self):
        (x, y, z) = (1, 2, 3)
        v = Vector((x,y,z))
        assert v.x == x
        assert v.y == y
        assert v.z == z

    def testCreate3dVectorInstanceWithHeadAndTailPointsAsTuples(self):
        (x0, y0, z0) = (1, 2, 7)
        (x1, y1, z1) = (5, -6, -4)
        v = Vector((x1,y1,z1), (x0,y0,z0))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == z1 - z0

    def testCreate3dVectorInstanceWithHeadAndTailPointsAsVectors(self):
        (x0, y0, z0) = (1, 2, -3)
        (x1, y1, z1) = (5, -6, 9)
        v = Vector(Vector((x1,y1,z1)), Vector((x0,y0,z0)))
        assert v.x == x1 - x0
        assert v.y == y1 - y0
        assert v.z == z1 - z0

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

    def test1dVectorHasLength1(self):
        v1 = Vector((5,))
        assert len(v1) == len(v1.coordinates) == 1
        v2 = Vector((5,0))
        assert len(v2) == len(v2.coordinates) == 1
        v3 = Vector((5,0,0))
        assert len(v3) == len(v3.coordinates) == 1

    def test2dVectorHasLength2(self):
        v = Vector((5,3))
        assert len(v) == len(v.coordinates) == 2

    def test3dVectorHasLength3(self):
        v = Vector((5,3,8))
        assert len(v) == len(v.coordinates) == 3


    def testVectorIsNotEqualToObjectWithDifferentType(self):
        assert Vector((5,5)) != (5,5)
        assert Vector((5,5)) != 5

    def testVectorsWithSameCoordinatesAreEqual(self):
        (x,y,z) = (3,2,10)

        assert Vector((x,y)) == Vector((x,y)) == Vector((x,y,0))
        assert Vector((x,y,z)) == Vector((x,y,z))
        assert Vector((-7,4,0)) == Vector((-7,4,0))
        assert not (Vector((-7,4,0)) != Vector((-7,4,0)))

    def testVectorsWithDifferentCoordinatesAreDifferent(self):
        assert Vector((5,3)) != Vector((3,5))
        assert Vector((5,3)) != Vector((5,3,9))

    def testHashCodeShouldBeAFunctionOfTheCoordinates(self):
        assert hash(Vector((5,5))) != hash(Vector((5,5.1)))
        assert hash(Vector((7,8))) != hash(Vector((7,8,9)))
        assert hash(Vector((7,8,9))) == hash(Vector((7,8,9)))

    def testToString(self):
        assert str(Vector((3,2,5))) == "Vector" + str((3,2,5))
        assert str(Vector((3,2))) == "Vector" + str((3,2))

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

    def testDotProductBetweenTwoVectors90DegreesAwayIsZero(self):
        v1 = Vector((0,50))
        v2 = Vector((100,0))
        assert v1.dotProduct(v2) == 0
        assert v2.dotProduct(v1) == 0


    def testPerpendicularDotProductBetween2dVectors(self):
        (v1,v2) = (3,4.23)
        v = Vector((v1,v2))
        (w1,w2) = (8.65,3.5)
        w = Vector((w1,w2))

        assert v.perpendicularDotProduct(w) == v.counterclockwiseRotationBy90Degrees().dotProduct(w)

    def testPerpendicularDotProductBetween3dVectorsIsNotImplemented(self):
        v = Vector((3,4.23,50))
        w = Vector((8.65,3.5,40))

        exceptionThrown = False
        try:
            v.perpendicularDotProduct(w)
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown


    def testClockwiseCrossProductBetweenTwo2dVectors90DegreesAwayHasNegativeZ(self):
        v1 = Vector((0,50))
        v2 = Vector((100,0))
        clockwise = v1.crossProduct(v2)
        assert clockwise[0] == 0
        assert clockwise[1] == 0
        assert clockwise[2] == -clockwise.norm == - (v1.norm * v2.norm) < 0

    def testCounterclockwiseCrossProductBetweenTwo2dVectors90DegreesAwayHasPositiveZ(self):
        v1 = Vector((0,50))
        v2 = Vector((100,0))
        counterclockwise = v2.crossProduct(v1)
        assert counterclockwise[0] == 0
        assert counterclockwise[1] == 0
        assert counterclockwise[2] == counterclockwise.norm == (v1.norm * v2.norm) > 0

    def testCrossProductBetweenCanonicalBasis(self):
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
        assert v.norm == math.sqrt(v1*v1 + v2*v2)

    def testNormOf3dVector(self):
        (v1,v2,v3) = (3,4,5)
        v = Vector((v1,v2,v3))
        assert v.norm == math.sqrt(v1*v1 + v2*v2 + v3*v3)


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
        assert mirror.tail == v.head
        assert mirror.head == v.tail
        assert v.norm == mirror.norm
        assert MathUtil.equalWithinError(v.angleBetween(mirror), math.pi, 0.0000001)

    def testReflectionFromReflectionIsTheOriginalVector(self):
        v = Vector((436,-13,40), (-950,30,2.35))
        mirror = v.reflection()
        assert mirror.reflection() == v


    def testVectorIsClockwiseDistanceFromAnoterVector(self):
        v1 = Vector((5,5))
        v2 = Vector((5,-5))
        assert v1.isClockwiseDistanceFrom(v2)
        assert not v2.isClockwiseDistanceFrom(v1)

    def testVectorIsCounterclockwiseDistanceFromAnoterVector(self):
        v1 = Vector((5,-5))
        v2 = Vector((5,5))
        assert v1.isCounterclockwiseDistanceFrom(v2)
        assert not v2.isCounterclockwiseDistanceFrom(v1)


    def testParallelVectorsAreAtBothClockwiseAndCouterclockwiseDistanceFromEachOther(self):
        a = 5
        v1 = Vector((a,a))
        v2 = Vector((2*a,2*a))
        assert v1.isClockwiseDistanceFrom(v2)
        assert v2.isCounterclockwiseDistanceFrom(v1)

        a = 5
        v1 = Vector((a,a))
        v2 = Vector((-2*a,-2*a))
        assert v1.isClockwiseDistanceFrom(v2)
        assert v2.isCounterclockwiseDistanceFrom(v1)

    def test45DegreeClockwiseRotationOf2dVector(self):
        radians = math.radians(45)
        a = 5
        v = Vector((a,0))
        clockwise = v.clockwiseRotationBy(radians)
        assert v.angleBetween(clockwise) == radians
        assert clockwise.isCounterclockwiseDistanceFrom(v)
        assert clockwise.norm == v.norm == a

    def test45DegreeCounterclockwiseRotationOf2dVector(self):
        radians = math.radians(45)
        a = 5
        v = Vector((a,0))
        counterclockwise = v.counterclockwiseRotationBy(radians)
        assert v.angleBetween(counterclockwise) == radians
        assert counterclockwise.isClockwiseDistanceFrom(v)
        assert counterclockwise.norm == v.norm == a

    def test90DegreeClockwiseRotationOf2dVector(self):
        v = Vector((3,2), (-1,-50))
        clockwise = v.clockwiseRotationBy90Degrees()
        assert clockwise.dotProduct(v) == 0
        assert clockwise.angleBetween(v) == math.pi/2
        assert clockwise.norm == v.norm
        assert clockwise == v.clockwiseRotationBy(math.pi/2)

    def test90DegreeClockwiseRotationIsClockwiseFor2dVector(self):
        a = 4
        v = Vector((0, a))
        assert v.clockwiseRotationBy90Degrees() == Vector((a,0))
        assert v.clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees() == Vector((0,-a))
        assert v.clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees() == Vector((-a,0))
        assert v.clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees().clockwiseRotationBy90Degrees() == v

    def test90DegreeClockwiseRotationOverCounterclockwiseRotationIsTheOriginal2dVector(self):
        v = Vector((312,460), (-93,517))
        counterclockwise = v.counterclockwiseRotationBy90Degrees()
        assert counterclockwise.clockwiseRotationBy90Degrees() == v

        v = Vector((312,460), (-93,517))
        counterclockwise = v.counterclockwiseRotationBy(math.pi/2)
        assert counterclockwise.clockwiseRotationBy(math.pi/2) == v


    def test90DegreeCounterclockwiseRotationFor2dVector(self):
        v = Vector((3,2), (-1,-50))
        counterclockwise = v.counterclockwiseRotationBy90Degrees()
        assert counterclockwise.dotProduct(v) == 0
        assert counterclockwise.angleBetween(v) == math.pi/2
        assert counterclockwise.norm == v.norm
        assert counterclockwise == v.counterclockwiseRotationBy(math.pi/2)

    def test90DegreeCounterclockwiseRotationIsCounterclockwiseFor2dVector(self):
        a = 4
        v = Vector((0, a))
        assert v.counterclockwiseRotationBy90Degrees() == Vector((-a, 0))
        assert v.counterclockwiseRotationBy90Degrees().counterclockwiseRotationBy90Degrees() == Vector((0, -a))
        assert v.counterclockwiseRotationBy90Degrees().counterclockwiseRotationBy90Degrees().counterclockwiseRotationBy90Degrees() == Vector((a, 0))
        assert v.counterclockwiseRotationBy90Degrees().counterclockwiseRotationBy90Degrees().counterclockwiseRotationBy90Degrees().counterclockwiseRotationBy90Degrees() == v

    def test90DegreeCounterclockwiseRotationOverClockwiseRotationIsTheOriginal2dVector(self):
        v = Vector((312,460), (-93,517))
        clockwise = v.clockwiseRotationBy90Degrees()
        assert clockwise.counterclockwiseRotationBy90Degrees() == v

        v = Vector((312,460), (-93,517))
        clockwise = v.clockwiseRotationBy(math.pi/2)
        assert clockwise.counterclockwiseRotationBy(math.pi/2) == v

    def test90DegreeClockwiseRotationIsNotImplementedFor3dVectors(self):
        v = Vector((5,7,9))
        exceptionThrown = False
        try:
            v.clockwiseRotationBy90Degrees()
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown

    def test90DegreeCounterclockwiseRotationIsNotImplementedFor2dVectors(self):
        v = Vector((5,7,9))
        exceptionThrown = False
        try:
            v.counterclockwiseRotationBy90Degrees()
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown

    def testClockwiseRotationIsNotImplementedFor3dVectors(self):
        v = Vector((5,7,9))
        exceptionThrown = False
        try:
            v.clockwiseRotationBy(math.pi)
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown

    def testCounterclockwiseRotationIsNotImplementedFor2dVectors(self):
        v = Vector((5,7,9))
        exceptionThrown = False
        try:
            v.counterclockwiseRotationBy(math.pi)
        except NotImplementedError:
            exceptionThrown = True
        assert exceptionThrown

    def test180DegreeClockwiseRotationOf2dVector(self):
        radians = math.pi
        a = 5
        v = Vector((a,0))
        clockwise = v.clockwiseRotationBy(radians)
        assert v.angleBetween(clockwise) == radians
        assert clockwise.isCounterclockwiseDistanceFrom(v)
        assert clockwise.norm == v.norm == a

    def test180DegreeCounterclockwiseRotationOf2dVector(self):
        radians = math.pi
        a = 5
        v = Vector((a,0))
        counterclockwise = v.counterclockwiseRotationBy(radians)
        assert v.angleBetween(counterclockwise) == radians
        assert counterclockwise.isClockwiseDistanceFrom(v)
        assert counterclockwise.norm == v.norm == a

    def testMultipliedByPositiveScalarWithZeroAsTail(self):
        head = (4, 32.3, 5.6, 0, 7)
        scalar = 5.3

        multipliedVector = Vector(head).multipliedByScalar(scalar)

        for i in xrange(len(head)):
            assert multipliedVector[i] == multipliedVector.head[i] == scalar * head[i]

        assert multipliedVector.tail == Point((0,))

    def testMultipliedByPositiveScalarWithNonZeroAsTail(self):
        head = (4, 32.3, 5)
        tail = (5, -2, 3.5)
        scalar = 5

        vector = Vector(head, tail)
        multipliedVector = vector.multipliedByScalar(scalar)

        for i in xrange(len(head)):
            assert multipliedVector[i] == scalar * vector[i]
        
        assert multipliedVector.tail == tail

    def testMultipliedByNegativeScalarWithZeroAsTail(self):
        head = (4, 32.3, 5.6, 0, 7)
        scalar = -5.3

        vector = Vector(head)
        multipliedVector = vector.multipliedByScalar(scalar)

        for i in xrange(len(head)):
            assert multipliedVector[i] == multipliedVector.head[i] == scalar * head[i]

        assert multipliedVector.tail == Point((0,))
        assert MathUtil.equalWithinError(multipliedVector.angleBetween(vector), math.pi, 0.0000001)

    def testMultipliedByPositiveScalarWithNonZeroAsTail(self):
        head = (4, 32.3, 5)
        tail = (5, -2, 3.5)
        scalar = 5

        vector = Vector(head, tail)
        multipliedVector = vector.multipliedByScalar(scalar)

        for i in xrange(len(head)):
            assert multipliedVector[i] == scalar * vector[i]
        
        assert multipliedVector.tail == tail

    def testMultipliedByNegativeScalarWithNonZeroAsTail(self):
        head = (4, 32.3, 5)
        tail = (5, -2, 3.5)
        scalar = -10.9

        vector = Vector(head, tail)
        multipliedVector = vector.multipliedByScalar(scalar)

        for i in xrange(len(head)):
            assert multipliedVector[i] == scalar * vector[i]
        
        assert multipliedVector.tail == tail
        assert MathUtil.equalWithinError(multipliedVector.angleBetween(vector), math.pi, 0.0000001)

    def testMultipliedByZero(self):
        head = (4, 32.3, 5)
        tail = (5, -2, 3.5)
        scalar = 0

        vector = Vector(head, tail)
        multipliedVector = vector.multipliedByScalar(scalar)

        for i in xrange(len(head)):
            assert multipliedVector[i] == scalar * vector[i]
        

        assert multipliedVector.tail == tail
        assert multipliedVector.head == multipliedVector.tail
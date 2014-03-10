import unittest
from unittest import TestCase

from ..geometry.Point import *

class PointTest(TestCase):

    def testPointCoordinatesShouldBeDimensionAgnostic(self):
        p1 = Point((1,2,3))
        assert p1[0] == p1.x == 1
        assert p1[1] == p1.y == 2
        assert p1[2] == p1.z == 3
        assert p1[3] == p1[4] == p1[5] == p1[6] == 0 # ...

        p2 = Point((1,2))
        assert p2[0] == p2.x == 1
        assert p2[1] == p2.y == 2
        assert p2[2] == p2.z == 0
        assert p2[3] == p2[4] == p2[5] == p2[6] == 0 # ...

        p3 = Point((1,))
        assert p3[0] == p3.x == 1
        assert p3[1] == p3.y == 0
        assert p3[2] == p3.z == 0
        assert p3[3] == p3[4] == p3[5] == p3[6] == 0 # ...

        p4 = Point()
        assert p4[0] == p4.x == 0
        assert p4[1] == p4.y == 0
        assert p4[2] == p4.z == 0
        assert p4[3] == p4[4] == p4[5] == p4[6] == 0 # ...

    def testEmptyPointIsEqualToZero(self):
        assert Point() == Point(()) == Point([]) == Point((0,)) == Point((0,0)) == Point((0,0,0))

    def testEqualPointsWithSameDimensionsAreEqual(self):
        assert Point((1,)) == Point((1,))
        assert Point((1,2.5)) == Point((1,2.5))
        assert Point((1,2,3.99)) == Point((1,2,3.99))
        assert Point((1,2,3.99,7)) == Point((1,2,3.99,7))

    def testEquivalentPointsWithDifferentDimensionsAreEqual(self):
        assert Point((1,)) == Point((1,0)) == Point((1,0,0)) == Point((1,0,0,0))
        assert Point((1,2)) == Point((1,2,0)) == Point((1,2,0,0)) == Point((1,2,0,0))
        assert Point((1,2,3)) == Point((1,2,3,0))

    def testSlightlyDifferentPointsWithSameDimensionsAreNotEqual(self):
        assert Point((1,2)) != Point((1,2.3))
        assert Point((0,2)) != Point((1,2))
        assert Point((1,2,3)) != Point((1,2,4))

    def testVeryDifferentPointsWithSameDimensionsAreNotEqual(self):
        assert Point((1,2)) != Point((66,50))
        assert Point((90.99,23)) != Point((1,2))
        assert Point((5,6,7)) != Point((1,2,4))

    def testSlightlyDifferentPointsWithDifferentDimensionsAreNotEqual(self):
        assert Point((1,)) != Point((1,2))
        assert Point((1,2)) != Point((0,2,0))
        assert Point((1,2,4)) != Point((1,2,3,0))
        assert Point((1,2)) != Point((1,2,0,3))

    def testVeryDifferentPointsWithDifferentDimensionsAreNotEqual(self):
        assert Point((1,)) != Point((1,38))
        assert Point((1,2)) != Point((0,673,0))
        assert Point((66,666,6666)) != Point((66,2,3,0))
        assert Point((7,8)) != Point((1,2,0,3))

    def testEqualityWithDuckTyping(self):
        assert Point((1,)) == (1,)
        assert Point((1,2,3)) == [1,2,3]
        assert Point((1,2)) == (1,2,0)

    def testHashCodeShouldBeAFunctionOfCoordinates(self):
        assert hash(Point((1,4))) == hash(Point((1,4)))
        assert hash(Point((88.3,99.5))) == hash(Point((88.3,99.5)))
        assert hash(Point((88.3,99.5))) != hash(Point((88.3,99.6)))
        assert hash(Point((88.3,99.5))) != hash(Point((88.4,99.5)))

    def testHashCodeShouldBeDimensionAgnostic(self):
        assert hash(Point((1,4))) == hash(Point((1,4,0))) == hash(Point((1,4,0,0)))
        assert hash(Point((88.3,99.5))) == hash(Point((88.3,99.5,0))) == hash(Point((88.3,99.5,0,0)))

    def testLengthOfZeroPointIsZero(self):
        assert len(Point()) == len(Point((0,))) == len(Point((0,0))) == len(Point((0,0,0))) == len(Point((0,0,0,0))) == 0

    def testLengthOfOneDimensionPointIsOne(self):
        assert len(Point((2,))) == len(Point((2,0))) == len(Point((2,0,0))) == 1

    def testLengthOfTwoDimensionPointIsTwo(self):
        assert len(Point((2,3))) == len(Point((2,3,0))) == len(Point((2,3,0,0))) == 2

    def testLengthOfThreeDimensionPointIsThree(self):
        assert len(Point((2,3,4))) == len(Point((2,3,4,0))) == len(Point((2,3,4,0))) == 3



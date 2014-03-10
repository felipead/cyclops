import unittest
from unittest import TestCase

from ..geometry.Square import *

class SquareTest(TestCase):
    
    def testSquareLength(self):
        a = 5
        square = Square([(0,a),(a,a),(a,0),(0,0)])
        assert square.sideLength == a

    def testSquareProjectionsOnlySupportQuadrilateralsAsInput(self):
        triangle = ConvexPolygon([(0,5), (5,5), (0,0)])
        exceptionThrown = False
        try:
            Square.projectQuadrilateral(triangle)
        except:
            exceptionThrown = True
        assert exceptionThrown

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheFirstPointUsingCounterclockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([a,b,c,d])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == a
        assert square[1] == b
        assert square[2] == new_c
        assert square[3] == new_d
        assert square.isClockwise == trapezoid.isClockwise == False

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheSecondPointUsingCounterclockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([d,a,b,c])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == new_d
        assert square[1] == a
        assert square[2] == b
        assert square[3] == new_c
        assert square.isClockwise == trapezoid.isClockwise == False

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheThirdPointUsingCounterclockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([c,d,a,b])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == new_c
        assert square[1] == new_d
        assert square[2] == a
        assert square[3] == b
        assert square.isClockwise == trapezoid.isClockwise == False

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheFourthPointUsingCounterclockwiseOrientation(self):
        b = (6,6)
        c = (4,1)
        d = (7,-4)
        a = (12,0)
        largestSide = Vector(a,b)
        new_c = (0,0)
        new_d = (6,-6)

        trapezoid = ConvexQuadrilateral([b,c,d,a])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == b
        assert square[1] == new_c
        assert square[2] == new_d
        assert square[3] == a
        assert square.isClockwise == trapezoid.isClockwise == False

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheFourthPointUsingClockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([d,c,b,a])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == new_d
        assert square[1] == new_c
        assert square[2] == b
        assert square[3] == a
        assert square.isClockwise == trapezoid.isClockwise == True

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheThirdPointUsingClockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([c,b,a,d])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == new_c
        assert square[1] == b
        assert square[2] == a
        assert square[3] == new_d
        assert square.isClockwise == trapezoid.isClockwise == True

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheSecondPointUsingClockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([b,a,d,c])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == b
        assert square[1] == a
        assert square[2] == new_d
        assert square[3] == new_c
        assert square.isClockwise == trapezoid.isClockwise == True

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheSecondPointUsingClockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([a,d,c,b])
        square = Square.projectQuadrilateral(trapezoid)
        assert square.sideLength == largestSide.norm
        assert square[0] == a
        assert square[1] == new_d
        assert square[2] == new_c
        assert square[3] == b
        assert square.isClockwise == trapezoid.isClockwise == True

    def testSquareProjectionsOfQuadrilateralAndItsMirrorAreEqual(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([a,b,c,d])
        square = Square.projectQuadrilateral(trapezoid)
        mirroredTrapezoid = ConvexQuadrilateral([a,d,c,b])
        mirroredSquare = Square.projectQuadrilateral(mirroredTrapezoid)
        assert mirroredSquare == square

    def testSquareProjectionOfSquareIsTheSquareItself(self):
        a = (0,0)
        b = (0,5)
        c = (5,5)
        d = (5,0)
        square = Square([a,b,c,d])

        assert Square.projectQuadrilateral(square) == square
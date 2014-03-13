import unittest
from unittest import TestCase

from ..geometry.Square import *
from ..geometry.Point import *

from ..util.MathUtil import *

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

    def testGetSquareCenter(self):
        a = (0,0)
        b = (0,6)
        c = (6,6)
        d = (6,0)
        square = Square([a,b,c,d])
        assert square.center == Point((3,3))

        a = (0,0)
        b = (-2,3)
        c = (1,5)
        d = (3,2)
        square = Square([a,b,c,d])
        assert square.center == Point((2.5,2.5))

    def testRotateCounterclockwiseSquare90DegreesCounterclockwiseWithoutPrecisionLoss(self):
        v1 = (0,2.5)
        v2 = (2.5,0)
        v3 = (5,2.5)
        v4 = (2.5,5)

        square = Square([v1, v2, v3, v4])
        rotated = square.counterclockwiseRotationBy90Degrees()

        assert rotated[0] == v2
        assert rotated[1] == v3
        assert rotated[2] == v4
        assert rotated[3] == v1

    def testRotateCounterclockwiseSquare90DegreesClockwiseWithoutPrecisionLoss(self):
        v1 = (0,2.5)
        v2 = (2.5,0)
        v3 = (5,2.5)
        v4 = (2.5,5)

        square = Square([v1, v2, v3, v4])
        rotated = square.clockwiseRotationBy90Degrees()

        assert rotated[0] == v4
        assert rotated[1] == v1
        assert rotated[2] == v2
        assert rotated[3] == v3

    def testRotateClockwiseSquare90DegreesCounterclockwiseWithoutPrecisionLoss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)

        square = Square([v1, v2, v3, v4])
        rotated = square.counterclockwiseRotationBy90Degrees()

        assert rotated[0] == v4
        assert rotated[1] == v1
        assert rotated[2] == v2
        assert rotated[3] == v3

    def testRotateClockwiseSquare90DegreesClockwiseWithoutPrecisionLoss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)
        
        square = Square([v1, v2, v3, v4])

        rotated = square.clockwiseRotationBy90Degrees()
        assert rotated[0] == v2
        assert rotated[1] == v3
        assert rotated[2] == v4
        assert rotated[3] == v1

    def test360DegreeRotationCanBeAchievedWithFour90DegreeClockwiseRotationsWithoutPrecisionLoss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)

        square = Square([v1, v2, v3, v4])        
        rotated = square.clockwiseRotationBy90Degrees()
        rotated = rotated.clockwiseRotationBy90Degrees()
        rotated = rotated.clockwiseRotationBy90Degrees()
        rotated = rotated.clockwiseRotationBy90Degrees()
        assert rotated == square

    def test360DegreeRotationCanBeAchievedWithFour90DegreeCounterclockwiseRotationsWithoutPrecisionLoss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)

        square = Square([v1, v2, v3, v4])        
        rotated = square.counterclockwiseRotationBy90Degrees()
        rotated = rotated.counterclockwiseRotationBy90Degrees()
        rotated = rotated.counterclockwiseRotationBy90Degrees()
        rotated = rotated.counterclockwiseRotationBy90Degrees()
        assert rotated == square

    def testRotate90DegreesClockwiseWithPrecisionLoss(self):
        angleInRadians = math.pi/2
        error = 0.000000001
        v1 = Point((0,2.5))
        v2 = Point((2.5,0))
        v3 = Point((5,2.5))
        v4 = Point((2.5,5))

        square = Square([v1, v2, v3, v4])
        rotated = square.clockwiseRotationBy(angleInRadians)

        assert MathUtil.equalWithinError(rotated[0].x, v4.x, error)
        assert MathUtil.equalWithinError(rotated[0].y, v4.y, error)
        assert MathUtil.equalWithinError(rotated[1].x, v1.x, error)
        assert MathUtil.equalWithinError(rotated[1].y, v1.y, error)
        assert MathUtil.equalWithinError(rotated[2].x, v2.x, error)
        assert MathUtil.equalWithinError(rotated[2].y, v2.y, error)
        assert MathUtil.equalWithinError(rotated[3].x, v3.x, error)
        assert MathUtil.equalWithinError(rotated[3].y, v3.y, error)

    def testRotateCounterclockwiseSquare45DegreesClockwiseWithPrecisionLoss(self):
        angleInRadians = math.pi/4
        error = 0.00001
        
        side = 5
        v1 = Point((0,0))
        v2 = Point((side,0))
        v3 = Point((side,side))
        v4 = Point((0,side))

        square = Square([v1, v2, v3, v4])
        assert not square.isClockwise
        rotated = square.clockwiseRotationBy(angleInRadians)

        for (originalSide,rotatedSide) in zip(square.contour,rotated.contour):
            assert MathUtil.equalWithinError(originalSide.angleBetween(rotatedSide), angleInRadians, error)
            assert originalSide.isClockwiseDistanceFrom(rotatedSide)

    def testRotateClockwiseSquare45DegreesClockwiseWithPrecisionLoss(self):
        angleInRadians = math.pi/4
        error = 0.000000001
        
        side = 5
        v1 = Point((0,0))
        v2 = Point((0,side))
        v3 = Point((side,side))
        v4 = Point((side,0))

        square = Square([v1, v2, v3, v4])
        assert square.isClockwise
        rotated = square.clockwiseRotationBy(angleInRadians)

        for (originalSide,rotatedSide) in zip(square.contour,rotated.contour):
            assert MathUtil.equalWithinError(originalSide.angleBetween(rotatedSide), angleInRadians, error)
            assert originalSide.isClockwiseDistanceFrom(rotatedSide)

    def testRotate90DegreesCounterclockwiseWithPrecisionLoss(self):
        angleInRadians = math.pi/2
        error = 0.0000000001
        v1 = Point((0,2.5))
        v2 = Point((2.5,0))
        v3 = Point((5,2.5))
        v4 = Point((2.5,5))

        square = Square([v1, v2, v3, v4])
        rotated = square.counterclockwiseRotationBy(angleInRadians)

        assert MathUtil.equalWithinError(rotated[0].x, v2.x, error)
        assert MathUtil.equalWithinError(rotated[0].y, v2.y, error)
        assert MathUtil.equalWithinError(rotated[1].x, v3.x, error)
        assert MathUtil.equalWithinError(rotated[1].y, v3.y, error)
        assert MathUtil.equalWithinError(rotated[2].x, v4.x, error)
        assert MathUtil.equalWithinError(rotated[2].y, v4.y, error)
        assert MathUtil.equalWithinError(rotated[3].x, v1.x, error)
        assert MathUtil.equalWithinError(rotated[3].y, v1.y, error)

    def testRotateCounterclockwiseSquare45DegreesCounterclockwiseWithPrecisionLoss(self):
        angleInRadians = math.pi/4
        error = 0.000000001
        
        side = 5
        v1 = Point((0,0))
        v2 = Point((side,0))
        v3 = Point((side,side))
        v4 = Point((0,side))

        square = Square([v1, v2, v3, v4])
        assert not square.isClockwise
        rotated = square.counterclockwiseRotationBy(angleInRadians)

        for (originalSide,rotatedSide) in zip(square.contour,rotated.contour):
            assert MathUtil.equalWithinError(originalSide.angleBetween(rotatedSide), angleInRadians, error)
            assert not originalSide.isClockwiseDistanceFrom(rotatedSide)

    def testRotateClockwiseSquare45DegreesCounterclockwiseWithPrecisionLoss(self):
        angleInRadians = math.pi/4
        error = 0.00001
        
        side = 5
        v1 = Point((0,0))
        v2 = Point((0,side))
        v3 = Point((side,side))
        v4 = Point((side,0))

        square = Square([v1, v2, v3, v4])
        assert square.isClockwise
        rotated = square.counterclockwiseRotationBy(angleInRadians)

        for (originalSide,rotatedSide) in zip(square.contour,rotated.contour):
            assert MathUtil.equalWithinError(originalSide.angleBetween(rotatedSide), angleInRadians, error)
            assert not originalSide.isClockwiseDistanceFrom(rotatedSide)

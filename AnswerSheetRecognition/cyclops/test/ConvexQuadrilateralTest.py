from ..geometry.ConvexQuadrilateral import *
from ..geometry.Vector import *
from ..util.MathUtil import *

from unittest import *
import math

class ConvexQuadrilateralTest(TestCase):

    def testCreateConvexQuadrilateral(self):
        v1 = (0,0)
        v2 = (0,15)
        v3 = (15,15)
        v4 = (15,0)
        quadrilateral = ConvexQuadrilateral([v1,v2,v3,v4])
        assert quadrilateral.isConvex

    def testCanNotCreateNonConvexQuadrilateral(self):
        v1 = (0,0)
        v2 = (3,6)
        v3 = (0,6)
        v4 = (4,2)
    
        exceptionThrown = False
        try:
            ConvexQuadrilateral((v1, v2, v3, v4))
        except:
            exceptionThrown = True

        assert exceptionThrown

    def testCanNotCreateQuadrilateralWithMoreThan4Vertexes(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)
        
        exceptionThrown = False
        try:
            ConvexQuadrilateral((v1, v2, v3, v4, v5))
        except:
            exceptionThrown = True

        assert exceptionThrown
    
    def testCanNotCreateQuadrilateralWithLessThan4Vertexes(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        
        exceptionThrown = False
        try:
            ConvexQuadrilateral((v1, v2, v3))
        except:
            exceptionThrown = True

        assert exceptionThrown

    def testExactSquareHasRightInteriorAngles(self):
        square = ConvexQuadrilateral([(0,0), (5,0), (5,5), (0,5)])
        assert square.hasRightInteriorAngles()

    def testExactRectangleHasRightInteriorAngles(self):
        rectangle = ConvexQuadrilateral([(0,0), (10,0), (10,5), (0,5)])
        assert rectangle.hasRightInteriorAngles()

    def testRoughSquareHasRouglhyRightInteriorAngles(self):
        d = 0.3
        roughSquare = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert roughSquare.hasRightInteriorAnglesWithRelaxationOf(0.2)

    def testTooRoughSquareDoesNotHaveRouglhyRightInteriorAngles(self):
        d = 0.7
        tooRoughSquare = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert not tooRoughSquare.hasRightInteriorAnglesWithRelaxationOf(0.2)

    def testTrapezoidDoesNotHaveRoughlyRightInteriorAngles(self):
        trapezoid = ConvexQuadrilateral([(1,-2), (13,4), (6,8), (-2,4)])
        assert not trapezoid.hasRightInteriorAnglesWithRelaxationOf(0.5)


    def testExactSquareHasEqualSides(self):
        square = ConvexQuadrilateral([(0,0), (5,0), (5,5), (0,5)])
        assert square.hasEqualSides()

    def testExactEquilateralLozengeHasEqualSides(self):
        lozenge = ConvexQuadrilateral([(0,0), (2,-1), (4,0), (2,1)])
        assert lozenge.hasEqualSides()

    def testRoughSquareHasRoughlyEqualSides(self):
        d = 0.3
        roughSquare = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert roughSquare.hasEqualSidesWithRelaxationRatioOf(1.15)

    def testTooRoughSquareDoesNotHaveRoughlyEqualSides(self):
        d = 2
        tooRoughSquare = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert not tooRoughSquare.hasEqualSidesWithRelaxationRatioOf(1.15)

    def testExactRectangleDoesNotHaveEqualSides(self):
        rectangle = ConvexQuadrilateral([(0,0), (7,0), (7,5), (0,5)])
        assert not rectangle.hasEqualSides()
        assert not rectangle.hasEqualSidesWithRelaxationRatioOf(1.15)

    def testTrapezoidDoesNotHaveRoughlyEqualSides(self):
        trapezoid = ConvexQuadrilateral([(1,-2), (13,4), (6,8), (-2,4)])
        assert not trapezoid.hasEqualSidesWithRelaxationRatioOf(1.15)

    def testReversedContourOfClockwiseQuadrilateral(self):
        a = (0,0)
        b = (0,1)
        c = (1,1)
        d = (1,0)
        square = ConvexQuadrilateral([a,b,c,d])
        reversedContour = square.reversedContour

        reversedVertexes = []
        for v in reversedContour:
            reversedVertexes.append(v.tail)

        assert reversedVertexes == [a,d,c,b]

    def testReversedContourOfCounterclockwiseQuadrilateral(self):
        a = (0,0)
        b = (1,0)
        c = (1,1)
        d = (0,1)
        square = ConvexQuadrilateral([a,b,c,d])
        reversedContour = square.reversedContour

        reversedVertexes = []
        for v in reversedContour:
            reversedVertexes.append(v.tail)

        assert reversedVertexes == [a,d,c,b]


    def testRotateCounterclockwiseSquare90DegreesCounterclockwiseWithoutPrecisionLoss(self):
        v1 = (0,2.5)
        v2 = (2.5,0)
        v3 = (5,2.5)
        v4 = (2.5,5)

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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
        
        square = ConvexQuadrilateral([v1, v2, v3, v4])

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

        square = ConvexQuadrilateral([v1, v2, v3, v4])        
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])        
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
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

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        assert square.isClockwise
        rotated = square.counterclockwiseRotationBy(angleInRadians)

        for (originalSide,rotatedSide) in zip(square.contour,rotated.contour):
            assert MathUtil.equalWithinError(originalSide.angleBetween(rotatedSide), angleInRadians, error)
            assert not originalSide.isClockwiseDistanceFrom(rotatedSide)

    def testProjectToSquareTrapezoidWithLargestSideStartingOnTheFirstPointUsingCounterclockwiseOrientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largestSide = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([a,b,c,d])
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        assert square.largestSideLength == largestSide.norm
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
        square = trapezoid.projectToSquare()
        mirroredTrapezoid = ConvexQuadrilateral([a,d,c,b])
        mirroredSquare = mirroredTrapezoid.projectToSquare()
        assert mirroredSquare == square

    def testSquareProjectionOfSquareIsTheSquareItself(self):
        a = (0,0)
        b = (0,5)
        c = (5,5)
        d = (5,0)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.projectToSquare() == square


    def testSquareLength(self):
        a = 5
        square = ConvexQuadrilateral([(0,a),(a,a),(a,0),(0,0)])
        assert square.largestSideLength == a



    def testCornersOfAlignedCounterclockwiseSquare(self):
        a = (0,0)
        b = (5,0)
        c = (5,5)
        d = (0,5)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.bottomLeftCorner == a
        assert square.bottomRightCorner == b
        assert square.topRightCorner == c
        assert square.topLeftCorner == d
    
    def testCornersOfAlignedClockwiseSquare(self):
        a = (0,0)
        b = (5,0)
        c = (5,5)
        d = (0,5)
        square = ConvexQuadrilateral([a,d,c,b])

        assert square.bottomLeftCorner == a
        assert square.bottomRightCorner == b
        assert square.topRightCorner == c
        assert square.topLeftCorner == d

    def testCornersOfMisalignedCounterclockwiseSquare(self):
        a = (6,6)
        b = (8,3)
        c = (11,5)
        d = (9,8)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOfMisalignedClockwiseSquare(self):
        a = (6,6)
        b = (8,3)
        c = (11,5)
        d = (9,8)
        square = ConvexQuadrilateral([a,d,c,b])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedCounterclockwiseSquareWithTopLeftAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedClockwiseSquareWithTopLeftAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([a,d,c,b])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedCounterclockwiseSquareWithTopRightAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([d,a,b,c])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedClockwiseSquareWithTopRightAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([d,c,b,a])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedCounterclockwiseSquareWithBottomRightAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([c,d,a,b])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedClockwiseSquareWithBottomRightAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([c,b,a,d])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedCounterclockwiseSquareWithBottomLeftAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([b,c,d,a])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOf45DegreesInclinatedClockwiseSquareWithBottomLeftAsFirstVertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([b,a,d,c])

        assert square.topLeftCorner == a
        assert square.bottomLeftCorner == b
        assert square.bottomRightCorner == c
        assert square.topRightCorner == d

    def testCornersOfCounterclockwiseTrapezoidWithTopLeftAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([a,b,c,d])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfClockwiseTrapezoidWithTopLeftAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([a,d,c,b])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfCounterclockwiseTrapezoidWithTopRightAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([d,a,b,c])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfClockwiseTrapezoidWithTopRightAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([d,c,b,a])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfCounterclockwiseTrapezoidWithBottomRightAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([c,d,a,b])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfClockwiseTrapezoidWithBottomRightAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([c,b,a,d])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfCounterclockwiseTrapezoidWithBottomLeftAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([b,c,d,a])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfClockwiseTrapezoidWithBottomLeftAsFirstVertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([b,a,d,c])

        assert trapezoid.topLeftCorner == a
        assert trapezoid.bottomLeftCorner == b
        assert trapezoid.bottomRightCorner == c
        assert trapezoid.topRightCorner == d

    def testCornersOfCounterclockwiseQuadrilateralWithThreeVertexesMatchingSquareProjection(self):
        a = (0,0)
        b = (4,0)
        c = (4,3)
        d = (2,2)
        trapezoid = ConvexQuadrilateral([a,b,c,d])

        assert trapezoid.topLeftCorner == d
        assert trapezoid.bottomLeftCorner == a
        assert trapezoid.bottomRightCorner == b
        assert trapezoid.topRightCorner == c

    def testCornersOfClockwiseQuadrilateralWithThreeVertexesMatchingSquareProjection(self):
        a = (0,0)
        b = (4,0)
        c = (4,3)
        d = (2,2)
        trapezoid = ConvexQuadrilateral([a,d,c,b])

        assert trapezoid.topLeftCorner == d
        assert trapezoid.bottomLeftCorner == a
        assert trapezoid.bottomRightCorner == b
        assert trapezoid.topRightCorner == c

    def testCornersOfClockwiseAndCounterclockwiseSquaresAreTheSame(self):
        a = (6,6)
        b = (8,3)
        c = (11,5)
        d = (9,8)
        counterclockwise = ConvexQuadrilateral([a,b,c,d])
        clockwise = ConvexQuadrilateral([a,d,c,b])

        assert clockwise.bottomLeftCorner == counterclockwise.bottomLeftCorner
        assert clockwise.topLeftCorner == counterclockwise.topLeftCorner
        assert clockwise.bottomRightCorner == counterclockwise.bottomRightCorner
        assert clockwise.topRightCorner == counterclockwise.topRightCorner

    def testCornersOfClockwiseAndCounterclockwiseTrapezoidsAreTheSame(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        counterclockwise = ConvexQuadrilateral([a,b,c,d])
        clockwise = ConvexQuadrilateral([a,d,c,b])

        assert clockwise.bottomLeftCorner == counterclockwise.bottomLeftCorner
        assert clockwise.topLeftCorner == counterclockwise.topLeftCorner
        assert clockwise.bottomRightCorner == counterclockwise.bottomRightCorner
        assert clockwise.topRightCorner == counterclockwise.topRightCorner

    def testCornersOfRandomQuadrilateral1(self):
        a = (197, 385)
        b = (345, 239)
        c = (197, 82)
        d = (55, 251)
        quadrilateral = ConvexQuadrilateral([a,b,c,d])

        assert quadrilateral.bottomLeftCorner == c
        assert quadrilateral.bottomRightCorner == b
        assert quadrilateral.topRightCorner == a
        assert quadrilateral.topLeftCorner == d

        reversedQuadrilateral = ConvexQuadrilateral([a,d,c,b])
        assert reversedQuadrilateral.bottomLeftCorner == c
        assert reversedQuadrilateral.bottomRightCorner == b
        assert reversedQuadrilateral.topRightCorner == a
        assert reversedQuadrilateral.topLeftCorner == d

    def testCornersOfRandomQuadrilateral2(self):
        a = (153, 346)
        b = (203, 98)
        c = (450, 96)
        d = (430, 370)
        quadrilateral = ConvexQuadrilateral([a,b,c,d])

        assert quadrilateral.bottomLeftCorner == b
        assert quadrilateral.bottomRightCorner == c
        assert quadrilateral.topRightCorner == d
        assert quadrilateral.topLeftCorner == a

        reversedQuadrilateral = ConvexQuadrilateral([a,d,c,b])
        assert reversedQuadrilateral.bottomLeftCorner == b
        assert reversedQuadrilateral.bottomRightCorner == c
        assert reversedQuadrilateral.topRightCorner == d
        assert reversedQuadrilateral.topLeftCorner == a
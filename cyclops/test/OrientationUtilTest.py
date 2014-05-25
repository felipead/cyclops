from unittest import *

from ..geometry.ConvexQuadrilateral import *
from ..util.OrientationUtil import *

class OrientationUtilTest(TestCase):
    
    def testShouldRotateClockwiseSquare270DegreesClockwiseIfOrientationCornerIsAtTheBottomLeftCorner(self):
        a = (0,0)
        b = (0,5)
        c = (5,5)
        d = (5,0)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 3
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([d,c,b,a])

    def testShouldRotateClockwiseSquare180DegreesClockwiseIfOrientationCornerIsAtTheTopLeftCorner(self):
        a = (0,5)
        b = (5,5)
        c = (5,0)
        d = (0,0)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 2
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([c,d,a,b])

    def testShouldRotateClockwiseSquare90DegreesClockwiseIfOrientationCornerIsAtTheTopRightCorner(self):
        a = (5,5)
        b = (5,0)
        c = (0,0)
        d = (0,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 1
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([b,c,d,a])

    def testShouldNotRotateClockwiseSquareIfOrientationCornerIsAtTheBottomRightCorner(self):
        a = (5,0)
        b = (0,0)
        c = (0,5)
        d = (5,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 0
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([a,b,c,d])

    def testShouldRotateCounterclockwiseSquare270DegreesClockwiseIfOrientationCornerIsAtTheBottomLeftCorner(self):
        a = (0,0)
        b = (5,0)
        c = (5,5)
        d = (0,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 3
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([b,c,d,a])

    def testShouldRotateCounterclockwiseSquare180DegreesClockwiseIfOrientationCornerIsAtTheTopLeftCorner(self):
        a = (0,5)
        b = (0,0)
        c = (5,0)
        d = (5,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 2
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([c,d,a,b])

    def testShouldRotateCounterclockwiseSquare90DegreesClockwiseIfOrientationCornerIsAtTheTopRightCorner(self):
        a = (5,5)
        b = (0,5)
        c = (0,0)
        d = (5,0)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 1
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([d,a,b,c])

    def testShouldNotRotateCounterclockwiseSquareIfOrientationCornerIsAtTheBottomRightCorner(self):
        a = (5,0)
        b = (0,0)
        c = (0,5)
        d = (5,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientationCorner = a

        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(square, orientationCorner)
        assert n == 0
        
        orientedSquare = OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(square, n)
        assert orientedSquare == ConvexQuadrilateral([a,b,c,d])
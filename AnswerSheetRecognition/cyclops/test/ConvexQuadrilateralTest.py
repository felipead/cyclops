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

    def testDoNotCreateNonConvexQuadrilateral(self):
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

    def testDoNotCreateQuadrilateralWithMoreThan4Vertexes(self):
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
    
    def testDoNotCreateQuadrilateralWithLessThan4Vertexes(self):
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

if __name__ == "__main__":
    unittest.main()

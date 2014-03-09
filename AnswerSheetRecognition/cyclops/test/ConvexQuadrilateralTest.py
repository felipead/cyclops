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
        assert quadrilateral.isConvex()

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
        assert roughSquare.hasRightInteriorAnglesWithRelaxation(0.2)

    def testTooRoughSquareDoesNotHaveRouglhyRightInteriorAngles(self):
        d = 0.7
        tooRoughSquare = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert not tooRoughSquare.hasRightInteriorAnglesWithRelaxation(0.2)

    def testTrapezoidDoesNotHaveRoughlyRightInteriorAngles(self):
        trapezoid = ConvexQuadrilateral([(1,-2), (13,4), (6,8), (-2,4)])
        assert not trapezoid.hasRightInteriorAnglesWithRelaxation(0.5)

    
    def testConvexQuadrilateralIsNotEqualToObjectWithDifferentType(self):
        v1 = (0,0)
        v2 = (5,0)
        v3 = (5,5)
        v4 = (0,5)
        quadrilateral = ConvexQuadrilateral([v1, v2, v3, v4])
        assert quadrilateral != 5

    def testConvexQuadrilateralsWithSameVertexesInTheSameOrderAreEqual(self):
        v1 = (0,0)
        v2 = (5,0)
        v3 = (5,5)
        v4 = (0,5)
        quadrilateral1 = ConvexQuadrilateral([v1, v2, v3, v4])
        quadrilateral2 = ConvexQuadrilateral([v1, v2, v3, v4])
        assert quadrilateral1 == quadrilateral2

    def testConvexQuadrilateralsWithSlightlyDifferentVertexesAreNotEqual(self):
        quadrilateral1 = ConvexQuadrilateral([(0,0), (5,0), (5,5), (0,5)])
        quadrilateral2 = ConvexQuadrilateral([(0,0), (6,0), (5,5), (0,5)])
        assert quadrilateral1 != quadrilateral2

    def testConvexQuadrilateralsWithVeryDifferentVertexesAreNotEqual(self):
        quadrilateral1 = ConvexQuadrilateral([(0,0), (5,0), (5,5), (0,5)])
        quadrilateral2 = ConvexQuadrilateral([(1,-2), (13,4), (6,8), (-2,4)])
        assert quadrilateral1 != quadrilateral2

    def testMirroredConvexQuadrilateralsAreEqual(self):
        v1 = (1,-2)
        v2 = (13,4)
        v3 = (6,8)
        v4 = (-2,4)
        quadrilateral1 = ConvexQuadrilateral([v1, v4, v3, v2])
        quadrilateral2 = ConvexQuadrilateral([v1, v2, v3, v4])
        assert quadrilateral1 == quadrilateral2

    def testHashCodeShouldBeDependentOnlyOnVertexesRegardlessOfTheOrder(self):
        v1 = (1,-2)
        v2 = (13,4)
        v3 = (6,8)
        v4 = (-2,4)
        quadrilateral1 = ConvexQuadrilateral([v1, v4, v3, v2])
        quadrilateral2 = ConvexQuadrilateral([v1, v2, v3, v4])
        quadrilateral3 = ConvexQuadrilateral([v4, v3, v2, v1])
        assert hash(quadrilateral1) == hash(quadrilateral2) == hash(quadrilateral3)

        quadrilateral4 = ConvexQuadrilateral([v1, v2, v3, (-3, 5)])
        quadrilateral5 = ConvexQuadrilateral([v1, (13.5,4.3), v3, (-3, 5)])
        quadrilateral6 = ConvexQuadrilateral([(0,-2), (13.5,4.3), v3, (-3, 5)])
        assert hash(quadrilateral1) != hash(quadrilateral4) != hash(quadrilateral5) != hash(quadrilateral6)

if __name__ == "__main__":
    unittest.main()

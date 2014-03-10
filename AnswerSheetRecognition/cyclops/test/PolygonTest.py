from ..geometry.Polygon import *
from ..geometry.Vector import *
from ..util.MathUtil import *
from ..util.Angles import *

from unittest import *
import math

class PolygonTest(TestCase):
    
    def testCanNotCreatePolygonWithLessThan3Vertexes(self):
        exceptionThrown = False
        try:
            Polygon([(1,2),(3,4)])
        except:
            exceptionThrown = True
        assert exceptionThrown

    def testCreatePolygonWith3Vertexes(self):
        v1 = (1,2)
        v2 = (2,3)
        v3 = (3,4)
        polygon = Polygon((v1, v2, v3))
        assert polygon[0] == polygon.vertexes[0] == v1
        assert polygon[1] == polygon.vertexes[1] == v2
        assert polygon[2] == polygon.vertexes[2] == v3
        assert len(polygon) == 3

    def testCreatePolygonWith5Vertexes(self):
        v1 = (1,2)
        v2 = (2,3)
        v3 = (3,4)
        v4 = (5,6)
        v5 = (7,8)
        polygon = Polygon((v1, v2, v3, v4, v5))
        assert polygon[0] == polygon.vertexes[0] == v1
        assert polygon[1] == polygon.vertexes[1] == v2
        assert polygon[2] == polygon.vertexes[2] == v3
        assert polygon[3] == polygon.vertexes[3] == v4
        assert polygon[4] == polygon.vertexes[4] == v5
        assert len(polygon) == 5

    def testGetSides(self):
        v1 = (1,2)
        v2 = (2,3)
        v3 = (3,4)
        v4 = (5,6)
        polygon = Polygon((v1, v2, v3, v4))
        assert polygon.sides == ((v1,v2),(v2,v3),(v3,v4),(v4,v1))

    def testGetContour(self):
        v1 = (1,2)
        v2 = (2,3)
        v3 = (3,4)
        v4 = (5,6)
        v5 = (7,8)
        polygon = Polygon((v1, v2, v3, v4, v5))
        assert polygon.contour == (Vector(v2,v1),Vector(v3,v2),Vector(v4,v3),Vector(v5,v4),Vector(v1,v5))

    def testSumOfSquareInteriorAnglesIs360Degrees(self):
        v1 = (0,0)
        v2 = (0,1)
        v3 = (1,1)
        v4 = (1,0)
        quadrilateral = Polygon((v1, v2, v3, v4))
        interiorAngles = quadrilateral.interiorAngles
        assert len(interiorAngles) == 4
        MathUtil.equalWithinError(sum(interiorAngles), Angles._360_DEGREES, 0.00000000000001)

    def testSumOfQuadrilateralInteriorAnglesIs360Degrees(self):
        v1 = (0,0)
        v2 = (7,0)
        v3 = (16,16)
        v4 = (14,3)
        quadrilateral = Polygon((v1, v2, v3, v4))
        interiorAngles = quadrilateral.interiorAngles
        assert len(interiorAngles) == 4
        MathUtil.equalWithinError(sum(interiorAngles), Angles._360_DEGREES, 0.00000000000001)

    def testSquareInteriorAnglesAre90Degrees(self):
        v1 = (0,0)
        v2 = (0,1)
        v3 = (1,1)
        v4 = (1,0)
        square = Polygon((v1, v2, v3, v4))
        interiorAngles = square.interiorAngles
        for angle in interiorAngles:
            assert angle == Angles._90_DEGREES

    def testSumOfTriangleInteriorAnglesIs180Degrees(self):
        v1 = (0,0)
        v2 = (5,6)
        v3 = (3,3)
        triangle = Polygon((v1, v2, v3))
        interiorAngles = triangle.interiorAngles
        assert len(interiorAngles) == 3
        assert MathUtil.equalWithinError(sum(interiorAngles), Angles._180_DEGREES, 0.00000000000001)

    def testRectangleTriangleAnglesAre45And90Degrees(self):
        v1 = (0,0)
        v2 = (15,15)
        v3 = (15,0)
        triangle = Polygon((v1, v2, v3))
        interiorAngles = triangle.interiorAngles
        assert MathUtil.equalWithinError(interiorAngles[0], Angles._45_DEGREES, 0.00000000000001)
        assert MathUtil.equalWithinError(interiorAngles[1], Angles._45_DEGREES, 0.00000000000001)
        assert MathUtil.equalWithinError(interiorAngles[2], Angles._90_DEGREES, 0.00000000000001)
        assert len(interiorAngles) == 3

    def testTriangleIsConvex(self):
        v1 = (0,0)
        v2 = (15,15)
        v3 = (15,0)
        triangle = Polygon((v1, v2, v3))
        assert triangle.isConvex

    def testDigonIsNotConvex(self):
        v1 = (0,0)
        v2 = (5,0)
        v3 = (7,0)
        digon = Polygon((v1, v2, v3))
        assert not digon.isConvex

    def testSquareIsConvex(self):
        v1 = (0,0)
        v2 = (0,15)
        v3 = (15,15)
        v4 = (15,0)
        rectangle = Polygon((v1, v2, v3, v4))
        assert rectangle.isConvex

    def testRectangleIsConvex(self):
        v1 = (0,0)
        v2 = (0,15)
        v3 = (10,15)
        v4 = (10,0)
        rectangle = Polygon((v1, v2, v3, v4))
        assert rectangle.isConvex

    def testTrapezoidIsConvex(self):
        v1 = (0,0)
        v2 = (7,0)
        v3 = (5,4)
        v4 = (2,4)
        quadrilateral = Polygon((v1, v2, v3, v4))
        assert quadrilateral.isConvex

    def testLozengeIsConvex(self):
        v1 = (0,0)
        v2 = (5,0)
        v3 = (8,4)
        v4 = (3,4)
        rectangle = Polygon((v1, v2, v3, v4))
        assert rectangle.isConvex

    def testConvexQuadrilateralIsConvex(self):
        v1 = (0,0)
        v2 = (7,0)
        v3 = (7,7)
        v4 = (2,5)
        quadrilateral = Polygon((v1, v2, v3, v4))
        assert quadrilateral.isConvex

    def testButterflyQuadrilateralIsNotConvex(self):
        v1 = (0,0)
        v2 = (3,6)
        v3 = (0,6)
        v4 = (4,2)
        quadrilateral = Polygon((v1, v2, v3, v4))
        assert not quadrilateral.isConvex

    def testQuadrilateralWithCollinearVertexesIsNotConvex(self):
        v1 = (0,0)
        v2 = (5,0)
        v3 = (8,0)
        v4 = (-5,6)
        polygon = Polygon((v1, v2, v3, v4))
        assert not polygon.isConvex

    def testConvexPentagonIsConvex(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)
        pentagon = Polygon((v1,v2,v3,v4,v5))
        assert pentagon.isConvex

    def testConcavePentagonIsNotConvex(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,1)
        v5 = (0,3)
        pentagon = Polygon((v1,v2,v3,v4,v5))
        assert not pentagon.isConvex

    def testConvexOctagonIsConvex(self):
        v1 = (0,0)
        v2 = (2,0)
        v3 = (3,2)
        v4 = (3,4)
        v5 = (2,6)
        v6 = (0,6)
        v7 = (-1,4)
        v8 = (-1,2)
        octagon = Polygon((v1, v2, v3, v4, v5, v6, v7, v8))
        assert octagon.isConvex

    def testConcaveOctagonIsNotConvex(self):
        v1 = (0,0)
        v2 = (2,0)
        v3 = (3,2)
        v4 = (3,4)
        v5 = (2,2)
        v6 = (0,2)
        v7 = (-1,4)
        v8 = (-1,2)
        octagon = Polygon((v1, v2, v3, v4, v5, v6, v7, v8))
        assert not octagon.isConvex

    def testPolygonsAreDifferentIfVertexesAreDifferentOrHaveDifferentOrder(self):
        assert Polygon([(1,2), (3,4), (5,6)]) != Polygon([(1,2), (99,100), (5,6)])
        assert Polygon([(1,2), (3,4), (5,6)]) != Polygon([(1,2), (5,6), (3,4)])
        assert Polygon([(1,2), (3,4), (5,6)]) != Polygon([(1,2), (3,4), (5,6), (7,8)])

    def testPolygonsAreEqualIfVertexesAreEqualInTheSameOrder(self):
        assert Polygon([(1,2), (3,4), (5,6)]) == Polygon([(1,2), (3,4), (5,6)]) == Polygon(((1,2), (3,4), (5,6)))

    def testHashCodeIsAFunctionOfVertexes(self):
        assert hash(Polygon([(1,2), (3,4), (5,6)])) != hash(Polygon([(1,2), (99,101), (5,6)]))
        assert hash(Polygon([(1,2), (3,4), (5,6)])) != hash(Polygon([(1,2), (5,6), (3,4)]))
        assert hash(Polygon([(1,2), (3,4), (5,6)])) != hash(Polygon([(1,2), (3,4), (5,6), (7,8)]))   

        assert hash(Polygon([(1,2), (3,4), (5,6)])) == hash(Polygon([(1,2), (3,4), (5,6)])) == hash(Polygon(((1,2), (3,4), (5,6))))


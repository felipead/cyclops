from ..geometry.ConvexPolygon import *
from ..geometry.Point import *

from unittest import *

class ConvexPolygonTest(TestCase):

    def testCreateConvexPolygon(self):
        v1 = (0,0)
        v2 = (0,15)
        v3 = (15,15)
        v4 = (15,0)
        convex = Polygon([v1,v2,v3,v4])
        assert convex.isConvex

    def testDoNotCreateConcavePolygon(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,1)
        v5 = (0,3)
        concave = Polygon([v1,v2,v3,v4,v5])
        assert not concave.isConvex

    def testConvexTriangleWithClockwiseContourIsClockwise(self):
        v1 = (0,0)
        v2 = (15,15)
        v3 = (15,0)
        triangle = ConvexPolygon((v1,v2,v3))
        assert triangle.isClockwise

    def testConvexTriangleWithCounterclockwiseContourIsCounterclockwise(self):
        v1 = (0,0)
        v2 = (15,15)
        v3 = (15,0)
        triangle = ConvexPolygon((v3,v2,v1))
        assert not triangle.isClockwise

    def testConvexPentagonWithCounterclockwiseContourIsNotClockwise(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)
        pentagon = ConvexPolygon((v1,v2,v3,v4,v5))
        assert not pentagon.isClockwise

    def testConvexPentagonWithClockwiseContourIsClockwise(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)
        pentagon = ConvexPolygon((v5,v4,v3,v2,v1))
        assert pentagon.isClockwise

    def testConvexPolygonIsNotEqualToObjectWithDifferentType(self):
        v1 = (0,0)
        v2 = (5,0)
        v3 = (5,5)
        v4 = (0,5)
        polygon = ConvexPolygon([v1, v2, v3, v4])
        assert polygon != 5

    def testConvexPolygonsWithSameVertexesInTheSameOrderAreEqual(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)
        polygon1 = ConvexPolygon([v1, v2, v3, v4, v5])
        polygon2 = ConvexPolygon([v1, v2, v3, v4, v5])
        assert polygon1 == polygon2

    def testConvexPolygonsWithSlightlyDifferentVertexesAreNotEqual(self):
        polygon1 = ConvexPolygon([(0,0), (5,0), (5,5), (0,5)])
        polygon2 = ConvexPolygon([(0,0), (6,0), (5,5), (0,5)])
        assert polygon1 != polygon2

    def testConvexPolygonsWithVeryDifferentVertexesAreNotEqual(self):
        polygon1 = ConvexPolygon([(0,0), (5,0), (5,5), (0,5)])
        polygon2 = ConvexPolygon([(1,-2), (13,4), (6,8), (-2,4)])
        assert polygon1 != polygon2

    def testConvexPolygonsWithDifferentNumberOfVertexesAreNotEqual(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)
        assert v1

    def testConvexTrianglesMirroredOverTheFirstVertexAreEqual(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (2,3)
        assert ConvexPolygon((v1,v2,v3)) == ConvexPolygon((v1,v3,v2))

    def testConvexQuadrilateralsMirroredOverTheFirstVertexAreEqual(self):
        v1 = (1,-2)
        v2 = (13,4)
        v3 = (6,8)
        v4 = (-2,4)
        polygon1 = ConvexPolygon([v1, v2, v3, v4])
        polygon2 = ConvexPolygon([v1, v4, v3, v2])
        assert polygon1 == polygon2

    def testConvexPentagonsMirroredOverTheFirstVertexAreEqual(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)
        assert ConvexPolygon((v1,v2,v3,v4,v5)) == ConvexPolygon((v1,v5,v4,v3,v2))

    def testHashCodeShouldBeDependentOnlyOnVertexesRegardlessOfTheOrder(self):
        v1 = (1,-2)
        v2 = (13,4)
        v3 = (6,8)
        v4 = (-2,4)
        polygon1 = ConvexPolygon([v1, v4, v3, v2])
        polygon2 = ConvexPolygon([v1, v2, v3, v4])
        polygon3 = ConvexPolygon([v4, v3, v2, v1])
        assert hash(polygon1) == hash(polygon2) == hash(polygon3)

        polygon4 = ConvexPolygon([v1, v2, v3, (-3, 5)])
        polygon5 = ConvexPolygon([v1, (13.5,4.3), v3, (-3, 5)])
        polygon6 = ConvexPolygon([(0,-2), (13.5,4.3), v3, (-3, 5)])
        assert hash(polygon1) != hash(polygon4) != hash(polygon5) != hash(polygon6)

    def testAreaOfSquare(self):
        a = 6
        v1 = (a,0)
        v2 = (a,a)
        v3 = (0,a)
        v4 = (0,0)
        assert ConvexPolygon([v1, v2, v3, v4]).area == a*a

    def testAreaOfRectangle(self):
        a = 6
        b = 12
        v1 = (a,0)
        v2 = (a,b)
        v3 = (0,b)
        v4 = (0,0)
        assert ConvexPolygon([v1, v2, v3, v4]).area == a*b

    def testAreaOfEquilateralTriangle(self):
        a = 6
        b = 12
        v1 = (0,0)
        v2 = (a,0)
        v3 = (a,b)
        assert ConvexPolygon([v1,v2,v3]).area == a*b*0.5

    def testAreaOfTrapezoid(self):
        a = 12
        b = 6
        height = b
        v1 = (0,0)
        v2 = (a,0)
        v3 = (a - b/float(2),b)
        v4 = (b/float(2),b)

        assert ConvexPolygon([v1,v2,v3,v4]).area == 0.5*(a+b) * b

    def testCentroidOfSquare(self):
        a = (0,0)
        b = (0,6)
        c = (6,6)
        d = (6,0)
        assert ConvexPolygon([a,b,c,d]).centroid == Point((3,3))

        a = (0,0)
        b = (-2,3)
        c = (1,5)
        d = (3,2)
        assert ConvexPolygon([a,b,c,d]).centroid == Point((0.5,2.5))

        a = (10,20)
        b = (13,17)
        c = (16,20)
        d = (13,23)
        assert ConvexPolygon([a,b,c,d]).centroid == Point((13,20))

    def testCentroidOfRectangle(self):
        a = (0,0)
        b = (0,12)
        c = (6,12)
        d = (6,0)
        assert ConvexPolygon([a,b,c,d]).centroid == Point((3,6))

    def testCentroidOfEquilateralLozenge(self):
        a = (0,0)
        b = (4,-2)
        c = (8,0)
        d = (4,2)
        assert ConvexPolygon([a,b,c,d]).centroid == Point((4,0))

    def testCentroidOfTrapezoid(self):
        a = 4
        b = 2
        v1 = (0,0)
        v2 = (1,2)
        v3 = (3,2)
        v4 = (4,0)
        centroid = ConvexPolygon([v1,v2,v3,v4]).centroid
        assert centroid == (2,1)

    def testCentroidOfEquilateralOctagon(self):
        v1 = (0,0)
        v2 = (1,-1)
        v3 = (2,-1)
        v4 = (3,0)
        v5 = (3,1)
        v6 = (2,2)
        v7 = (1,2)
        v8 = (0,1)
        octagon = ConvexPolygon([v1,v2,v3,v4,v5,v6,v7,v8])
        assert octagon.centroid == (1.5,0.5)

    def testCentroidOfIsocelesTriangle(self):
        v1 = (0,0)
        v2 = (3,0)
        v3 = (1.5, 3)
        triangle = ConvexPolygon([v1,v2,v3])
        centroid = triangle.centroid
        assert centroid.x == 1.5
        assert centroid.y == 1

    def testCentroidOfDeformedQuadrilateral(self):
        v1 = (1,5)
        v2 = (2,3)
        v3 = (7,5)
        v4 = (4,8)
        quadrilateral = ConvexPolygon([v1,v2,v3,v4])
        centroid = quadrilateral.centroid
        assert centroid.x > 3 and centroid.x < 4
        assert centroid.y > 5 and centroid.y < 5.5
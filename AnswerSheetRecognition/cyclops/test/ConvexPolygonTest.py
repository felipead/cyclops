from ..geometry.ConvexPolygon import *

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

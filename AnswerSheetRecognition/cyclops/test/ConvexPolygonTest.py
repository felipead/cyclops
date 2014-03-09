from ..geometry.ConvexPolygon import *

from unittest import *

class ConvexPolygonTest(TestCase):

    def testCreateConvexPolygon(self):
        v1 = (0,0)
        v2 = (0,15)
        v3 = (15,15)
        v4 = (15,0)
        convex = Polygon([v1,v2,v3,v4])
        assert convex.isConvex()

    def testDoNotCreateConcavePolygon(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,1)
        v5 = (0,3)
        concave = Polygon([v1,v2,v3,v4,v5])
        assert not concave.isConvex()
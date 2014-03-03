from ..QuadrilateralPolygon import *
from ..MathUtil import *
from ..Vector import *

from unittest import *
import math

class QuadrilateralPolygonTest(TestCase):

    def testShapeWithMoreThanFourVertexesIsNotConvexQuadrilateral(self):
        vertexes = [(0,0), (1,1), (2,2), (3,3), (4,4)]
        relaxation = 1

        exceptionThrown = False
        try:
            QuadrilateralPolygon(vertexes)
        except:
            exceptionThrown = True

        assert exceptionThrown

    def testShapeWithLessThanFourVertexesIsNotConvexQuadrilateral(self):
        vertexes = [(0,0), (3,3), (5,5)]
        relaxation = 1
        
        exceptionThrown = False
        try:
            QuadrilateralPolygon(vertexes)
        except:
            exceptionThrown = True

        assert exceptionThrown

    def testConcaveShapeWithFourLinesIsNotConvexQuadrilateral(self):
        vertexes = [(0,0), (3,3), (5,5), (6, 3)]
        relaxation = 0.2
        assert not QuadrilateralPolygon(vertexes).isConvexWithRoughlyRightAngles(relaxation)

    def testExactSquareIsConvexQuadrilateralWithRoughlyEqualAngles(self):
        vertexes = [(0,0), (5,0), (5,5), (0,5)]
        relaxation = 0
        assert QuadrilateralPolygon(vertexes).isConvexWithRoughlyRightAngles(relaxation)

    def testRoughSquareIsConvexQuadrilateralWithRoughlyEqualAngles(self):
        d = 0.3
        vertexes = [(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)]
        relaxation = 0.2
        assert QuadrilateralPolygon(vertexes).isConvexWithRoughlyRightAngles(relaxation)

    def testTooRoughSquareIsNotConvexQuadrilateralWithRoughlyEqualAngles(self):
        d = 0.7
        vertexes = [(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)]
        relaxation = 0.2
        assert not QuadrilateralPolygon(vertexes).isConvexWithRoughlyRightAngles(relaxation)

    def testTrapezoidIsNotConvexQuadrilateralWithRoughlyEqualAngles(self):
        vertexes = [(1,-2), (13,4), (6,8), (-2,4)]
        relaxation = 0.5
        assert not QuadrilateralPolygon(vertexes).isConvexWithRoughlyRightAngles(relaxation)


    def testOneExactRightAngleIsRoughlyRight(self):
        rightAngle = math.pi/2
        assert QuadrilateralPolygon._areAnglesRoughlyRight([rightAngle], 0)

    def testOneRoughRightAngleIsRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0.2
        assert QuadrilateralPolygon._areAnglesRoughlyRight([rightAngle + relaxation], relaxation)

    def testOneAcuteAngleIsNotRoughlyRight(self):
        relaxation = 0.2
        assert not QuadrilateralPolygon._areAnglesRoughlyRight([math.pi/4], relaxation)

    def testOneObtuseAngleIsNotRoughlyRight(self):
        relaxation = 0.2
        assert not QuadrilateralPolygon._areAnglesRoughlyRight([3*math.pi/4], relaxation)

    def testFourExactRightAnglesAreRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0
        angles = [rightAngle, rightAngle, rightAngle, rightAngle]
        assert QuadrilateralPolygon._areAnglesRoughlyRight(angles, relaxation)

    def testFourRoughRightAnglesAreRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0.2
        angles = [rightAngle - relaxation/2, rightAngle + relaxation/2, rightAngle - relaxation, rightAngle + relaxation]
        assert QuadrilateralPolygon._areAnglesRoughlyRight(angles, relaxation)

    def testFourTooRoughRightAnglesAreNotRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0.2
        angles = [rightAngle - relaxation*1.2, rightAngle, rightAngle - relaxation*1.2, rightAngle]
        assert not QuadrilateralPolygon._areAnglesRoughlyRight(angles, relaxation)

if __name__ == "__main__":
    unittest.main()

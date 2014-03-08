from ..geometry.Quadrilateral import *
from ..geometry.Vector import *
from ..util.MathUtil import *

from unittest import *
import math

class QuadrilateralTest(TestCase):

    def testShapeWithMoreThanFourVertexesIsNotQuadrilateral(self):
        vertexes = [(0,0), (1,1), (2,2), (3,3), (4,4)]
        relaxation = 1

        exceptionThrown = False
        try:
            Quadrilateral(vertexes)
        except:
            exceptionThrown = True

        assert exceptionThrown

    def testShapeWithLessThanFourVertexesIsNotQuadrilateral(self):
        vertexes = [(0,0), (3,3), (5,5)]
        relaxation = 1
        
        exceptionThrown = False
        try:
            Quadrilateral(vertexes)
        except:
            exceptionThrown = True

        assert exceptionThrown

    def testConcaveShapeWithFourVertexesIsNotConvexQuadrilateral(self):
        shape = Quadrilateral([(0,0), (4,2), (1,4), (3, 0)], 0.2)
        assert not shape.isConvex()

    def testExactSquareIsConvexQuadrilateralWithRoughlyRightAngles(self):
        square = Quadrilateral([(0,0), (5,0), (5,5), (0,5)], 0)
        assert square.isConvex()
        assert square.isConvexWithRoughlyRightAngles()

    def testRoughSquareIsConvexQuadrilateralWithRoughlyRightAngles(self):
        d = 0.3
        roughSquare = Quadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)], 0.2)
        assert roughSquare.isConvex()
        assert roughSquare.isConvexWithRoughlyRightAngles()

    def testTooRoughSquareIsConvexQuadrilateralWithoutRightAngles(self):
        d = 0.7
        shape = Quadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)], 0.2)
        assert shape.isConvex()
        assert not shape.isConvexWithRoughlyRightAngles()

    def testTrapezoidIsConvexQuadrilateralWithoutRightAngles(self):
        shape = Quadrilateral([(1,-2), (13,4), (6,8), (-2,4)], 0.5)
        assert shape.isConvex()
        assert not shape.isConvexWithRoughlyRightAngles()


    def testOneExactRightAngleIsRoughlyRight(self):
        rightAngle = math.pi/2
        assert Quadrilateral._areAnglesRoughlyRight([rightAngle], 0)

    def testOneRoughRightAngleIsRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0.2
        assert Quadrilateral._areAnglesRoughlyRight([rightAngle + relaxation], relaxation)

    def testOneAcuteAngleIsNotRoughlyRight(self):
        relaxation = 0.2
        assert not Quadrilateral._areAnglesRoughlyRight([math.pi/4], relaxation)

    def testOneObtuseAngleIsNotRoughlyRight(self):
        relaxation = 0.2
        assert not Quadrilateral._areAnglesRoughlyRight([3*math.pi/4], relaxation)

    def testFourExactRightAnglesAreRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0
        angles = [rightAngle, rightAngle, rightAngle, rightAngle]
        assert Quadrilateral._areAnglesRoughlyRight(angles, relaxation)

    def testFourRoughRightAnglesAreRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0.2
        angles = [rightAngle - relaxation/2, rightAngle + relaxation/2, rightAngle - relaxation, rightAngle + relaxation]
        assert Quadrilateral._areAnglesRoughlyRight(angles, relaxation)

    def testFourTooRoughRightAnglesAreNotRoughlyRight(self):
        rightAngle = math.pi/2
        relaxation = 0.2
        angles = [rightAngle - relaxation*1.2, rightAngle, rightAngle - relaxation*1.2, rightAngle]
        assert not Quadrilateral._areAnglesRoughlyRight(angles, relaxation)

    def testQuadrilateralIsNotEqualToObjectWithOtherType(self):
        v1 = (1,2)
        v2 = (3,4)
        v3 = (5,6)
        v4 = (7,8)
        angleRelaxation = 0.1
        quadrilateral = Quadrilateral([v1, v2, v3, v4], angleRelaxation)
        assert quadrilateral != 5

    def testQuadrilateralsWithSameVertexesInTheSameOrderAreEqual(self):
        v1 = (1,2)
        v2 = (3,4)
        v3 = (5,6)
        v4 = (7,8)
        angleRelaxation = 0.1
        quadrilateral1 = Quadrilateral([v1, v2, v3, v4], angleRelaxation)
        quadrilateral2 = Quadrilateral([v1, v2, v3, v4], angleRelaxation)

        assert quadrilateral1 == quadrilateral2

    def testQuadrilateralsWithSlightlyDifferentVertexesAreNotEqualDespiteAngleRelaxation(self):
        angleRelaxation = 0.1
        quadrilateral1 = Quadrilateral([(1,2), (3,4.5), (5,6), (7,8)], angleRelaxation)
        quadrilateral2 = Quadrilateral([(1,2), (3,4.4), (5,6), (7,8)], angleRelaxation)

        assert quadrilateral1 != quadrilateral2

    def testQuadrilateralsWithVeryDifferentVertexesAreNotEqual(self):
        angleRelaxation = 0.1
        quadrilateral1 = Quadrilateral([(1,2), (3,4), (5,6), (7,8)], angleRelaxation)
        quadrilateral2 = Quadrilateral([(9,10), (10,11), (11,12), (13,14)], angleRelaxation)

        assert quadrilateral1 != quadrilateral2

    def testMirroredConvexQuadrilateralsAreEqual(self):
        v1 = (1,2)
        v2 = (3,4)
        v3 = (5,6)
        v4 = (7,8)
        angleRelaxation = 0.1
        quadrilateral1 = Quadrilateral([v1, v4, v3, v2], angleRelaxation)
        quadrilateral2 = Quadrilateral([v1, v2, v3, v4], angleRelaxation)
        
        assert quadrilateral1 == quadrilateral2

    def testHashCodeShouldBeDependentOnlyOnVertexesRegardlessOfTheOrder(self):
        v1 = (1,2)
        v2 = (3,4)
        v3 = (5,6)
        v4 = (7,8)
        angleRelaxation = 0.1
        quadrilateral1 = Quadrilateral([v1, v4, v3, v2], 0.1)
        quadrilateral2 = Quadrilateral([v1, v2, v3, v4], 0.5)
        quadrilateral3 = Quadrilateral([v4, v3, v2, v1], 0.2)
        assert hash(quadrilateral1) == hash(quadrilateral2) == hash(quadrilateral3)

        quadrilateral4 = Quadrilateral([v1, v2, v3, (5, 10)], 0.1)
        quadrilateral5 = Quadrilateral([v1, (0,0), v3, (5, 10)], 0.1)
        quadrilateral6 = Quadrilateral([(999,256), (0,0), v3, (5, 10)], 0.1)
        assert hash(quadrilateral1) != hash(quadrilateral4) != hash(quadrilateral5) != hash(quadrilateral6)


    def testEdges(self):
        v1 = (1,2)
        v2 = (3,4)
        v3 = (5,6)
        v4 = (7,8)

        quadrilateral = Quadrilateral([v1, v2, v3, v4])
        assert quadrilateral.edges == [(v1,v2), (v2,v3), (v3,v4), (v4,v1)]

if __name__ == "__main__":
    unittest.main()

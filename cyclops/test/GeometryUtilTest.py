from unittest import *

from ..geometry.Vector import *
from ..geometry.ConvexQuadrilateral import *
from ..util.GeometryUtil import *

class GeometryUtilTest(TestCase):

    def testCreateSquareCounterclockwiseFromBottomToTopUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(bottomLeft, bottomRight)
        assert square == ConvexQuadrilateral([bottomLeft, bottomRight, topRight, topLeft])

    def testCreateSquareCounterclockwiseFromLeftToRightUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(topLeft, bottomLeft)
        assert square == ConvexQuadrilateral([topLeft, bottomLeft, bottomRight, topRight])

    def testCreateSquareCounterclockwiseFromRightToLeftUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(bottomRight, topRight)
        assert square == ConvexQuadrilateral([bottomRight, topRight, topLeft, bottomLeft])

    def testCreateSquareCounterclockwiseFromTopToBottomUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(topRight, topLeft)
        assert square == ConvexQuadrilateral([topRight, topLeft, bottomLeft, bottomRight])


    def testCreateSquareCounterclockwiseFromBottomToTopUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(bottomLeft, bottomRight)
        assert square == ConvexQuadrilateral([bottomLeft, bottomRight, topRight, topLeft])

    def testCreateSquareCounterclockwiseFromLeftToRightUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(topLeft, bottomLeft)
        assert square == ConvexQuadrilateral([topLeft, bottomLeft, bottomRight, topRight])

    def testCreateSquareCounterclockwiseFromRightToLeftUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(bottomRight, topRight)
        assert square == ConvexQuadrilateral([bottomRight, topRight, topLeft, bottomLeft])

    def testCreateSquareCounterclockwiseFromTopToBottomUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareCounterclockwiseFromTwoPoints(topRight, topLeft)
        assert square == ConvexQuadrilateral([topRight, topLeft, bottomLeft, bottomRight])

    def testCreateSquareClockwiseFromTopToBottomUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(topLeft, topRight)
        assert square == ConvexQuadrilateral([topLeft, topRight, bottomRight, bottomLeft])

    def testCreateSquareClockwiseFromLeftToRightUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(bottomLeft, topLeft)
        assert square == ConvexQuadrilateral([bottomLeft, topLeft, topRight, bottomRight])

    def testCreateSquareClockwiseFromRightToLeftUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(topRight, bottomRight)
        assert square == ConvexQuadrilateral([topRight, bottomRight, bottomLeft, topLeft])

    def testCreateSquareClockwiseFromBottomToTopUsingPointsParallelToAxis(self):
        a = 7.3
        bottomLeft = (0,0)
        bottomRight = (a,0)
        topRight = (a,a)
        topLeft = (0,a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(bottomRight, bottomLeft)
        assert square == ConvexQuadrilateral([bottomRight, bottomLeft, topLeft, topRight])

    def testCreateSquareClockwiseFromBottomToTopUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(bottomRight, bottomLeft)
        assert square == ConvexQuadrilateral([bottomRight, bottomLeft, topLeft, topRight])

    def testCreateSquareClockwiseFromLeftToRightUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(bottomLeft, topLeft)
        assert square == ConvexQuadrilateral([bottomLeft, topLeft, topRight, bottomRight])

    def testCreateSquareClockwiseFromRightToLeftUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(topRight, bottomRight)
        assert square == ConvexQuadrilateral([topRight, bottomRight, bottomLeft, topLeft])

    def testCreateSquareClockwiseFromTopToBottomUsingPointsNotParallelToAxis(self):
        a = 2
        bottomLeft = (0,a)
        bottomRight = (a,0)
        topRight = (2*a,a)
        topLeft = (a,2*a)

        square = GeometryUtil.createSquareClockwiseFromTwoPoints(topLeft, topRight)
        assert square == ConvexQuadrilateral([topLeft, topRight, bottomRight, bottomLeft])
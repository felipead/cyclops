from ..geometry.Vector import *

from ..geometry.ConvexQuadrilateral import *

class GeometryUtil:

    @staticmethod
    def createSquareClockwiseFromTwoPoints(topLeftPoint, topRightPoint):

        topRightToTopLeft = Vector(topLeftPoint, topRightPoint)

        topRightToBottomRight = topRightToTopLeft.counterclockwiseRotationBy90Degrees()
        topLeftToBottomLeft = reversed(topRightToTopLeft).clockwiseRotationBy90Degrees()

        bottomLeft = topLeftToBottomLeft.head
        topLeft = topLeftToBottomLeft.tail
        bottomRight = topRightToBottomRight.head
        topRight = topRightToBottomRight.tail

        return ConvexQuadrilateral((topLeft, topRight, bottomRight, bottomLeft))

    @staticmethod
    def createSquareCounterclockwiseFromTwoPoints(bottomLeftPoint, bottomRightPoint):

        bottomRightToBottomLeft = Vector(bottomLeftPoint, bottomRightPoint)

        bottomRightToTopRight = bottomRightToBottomLeft.clockwiseRotationBy90Degrees()
        bottomLeftToTopLeft = reversed(bottomRightToBottomLeft).counterclockwiseRotationBy90Degrees()

        bottomLeft = bottomLeftToTopLeft.tail
        topLeft = bottomLeftToTopLeft.head
        bottomRight = bottomRightToTopRight.tail
        topRight = bottomRightToTopRight.head

        return ConvexQuadrilateral((bottomLeft, bottomRight, topRight, topLeft))
from Vector import *
from MathUtil import *

import math

class QuadrilateralPolygon:

    def __init__(self, vertexes):
        if len(vertexes) != 4:
            raise Exception("Quadrilateral polygon must have exactly 4 vertexes.")
        self.vertexes = vertexes

    def isConvexWithRoughlyRightAngles(self, angleRelaxationInRadians):
        vertex1, vertex2, vertex3, vertex4 = self.vertexes
        angle1 = self._getAngleBetweenVertexes(vertex1, vertex4, vertex2)
        angle2 = self._getAngleBetweenVertexes(vertex2, vertex1, vertex3)
        angle3 = self._getAngleBetweenVertexes(vertex3, vertex2, vertex4)
        angle4 = self._getAngleBetweenVertexes(vertex4, vertex3, vertex1)
        sumOfInternalAngles = angle1 + angle2 + angle3 + angle4

        isConvexQuadrilateral = MathUtil.equalWithinError(sumOfInternalAngles, 2*math.pi, angleRelaxationInRadians*4)
        if isConvexQuadrilateral: 
            return self._areAnglesRoughlyRight([angle1, angle2, angle3, angle4], angleRelaxationInRadians)
        else:
            return False

    @staticmethod
    def _areAnglesRoughlyRight(angles, relaxationInRadians):
        rightAngle = math.pi/2
        for angle in angles:
            if angle < (rightAngle - relaxationInRadians) or angle > (rightAngle + relaxationInRadians):
                return False
        return True

    @staticmethod
    def _getAngleBetweenVertexes(angleVertex, vertex1, vertex2):
        v1 = Vector.create(angleVertex, vertex1)
        v2 = Vector.create(angleVertex, vertex2)
        return v1.angleBetween(v2)

    def __eq__(self, other):
        return self.vertexes == other.vertexes

    def __str__(self):
        return str(self.vertexes)
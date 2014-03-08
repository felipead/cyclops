from Vector import *
from ..util.MathUtil import *

import math

class Quadrilateral:

    def __init__(self, vertexes, angleRelaxationInRadians=0):
        if len(vertexes) != 4:
            raise Exception("Quadrilateral must have exactly 4 vertexes.")
        self._vertexes = vertexes
        self._angleRelaxationInRadians = angleRelaxationInRadians
        self._vertexAngles = Quadrilateral._calculateVertexAngles(self._vertexes)

    @property
    def vertexes(self):
        return list(self._vertexes)

    @property
    def vertexAngles(self):
        return list(self._vertexAngles)

    @property
    def edges(self):
        [v1, v2, v3, v4] = self._vertexes
        return [(v1,v2), (v2,v3), (v3,v4), (v4,v1)]

    def isConvex(self):
        return MathUtil.equalWithinError(sum(self._vertexAngles), 2*math.pi, self._angleRelaxationInRadians*4)

    def isConvexWithRoughlyRightAngles(self):
        if self.isConvex():
            return Quadrilateral._areAnglesRoughlyRight(self._vertexAngles, self._angleRelaxationInRadians)
        else:
            return False

    @staticmethod
    def _calculateVertexAngles(vertexes):
        vertex1, vertex2, vertex3, vertex4 = vertexes
        angle1 = Quadrilateral._getAngleBetweenVertexes(vertex1, vertex4, vertex2)
        angle2 = Quadrilateral._getAngleBetweenVertexes(vertex2, vertex1, vertex3)
        angle3 = Quadrilateral._getAngleBetweenVertexes(vertex3, vertex2, vertex4)
        angle4 = Quadrilateral._getAngleBetweenVertexes(vertex4, vertex3, vertex1)
        return [angle1, angle2, angle3, angle4]

    @staticmethod
    def _areAnglesRoughlyRight(angles, relaxationInRadians):
        rightAngle = math.pi/2
        for angle in angles:
            if angle < (rightAngle - relaxationInRadians) or angle > (rightAngle + relaxationInRadians):
                return False
        return True

    @staticmethod
    def _getAngleBetweenVertexes(cornerVertex, vertex1, vertex2):
        v1 = Vector(cornerVertex, vertex1)
        v2 = Vector(cornerVertex, vertex2)
        return v1.angleBetween(v2)

    def __eq__(self, other):
        if not isinstance(other, Quadrilateral):
            return False

        if self._vertexes == other._vertexes:
            return True

        if self.isConvex() and other.isConvex():
            if self._vertexes[0] == other._vertexes[0] and self._vertexes[2] == other._vertexes[2]:
                if self._vertexes[1] == other._vertexes[3] and self._vertexes[3] == other._vertexes[1]:
                    return True

        return False

    def __hash__(self):
        hashValue = 0
        for v in self._vertexes:
             hashValue ^= hash(v)
        return hashValue

    def __str__(self):
        return str(self._vertexes)
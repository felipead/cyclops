# -*- coding: utf-8 -*-

import math

class Vector:

    def __init__(self, terminalPoint, initialPoint=(0,0,0)):
        self._terminalPoint = Vector.__expandTo3dCoordinates(terminalPoint)
        self._initialPoint = Vector.__expandTo3dCoordinates(initialPoint)
        self._coordinates = (self._terminalPoint[0] - self._initialPoint[0], \
                             self._terminalPoint[1] - self._initialPoint[1], \
                             self._terminalPoint[2] - self._initialPoint[2])

    @staticmethod
    def __expandTo3dCoordinates(coordinates):
        if len(coordinates) == 2:
            return (coordinates[0], coordinates[1], 0)
        elif len(coordinates) == 3:
            return coordinates
        else:
            raise NotImplementedError("Only 2D and 3D vectors are supported.")

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

    @property
    def z(self):
        return self._coordinates[2]

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def initialPoint(self):
        return self._initialPoint

    @property
    def terminalPoint(self):
        return self._terminalPoint

    def dotProduct(self, anotherVector):
        dotProduct = 0
        for (i,j) in zip(self,anotherVector):
            dotProduct += i*j
        return dotProduct

    """
    The "perp dot product" (a^⊥ · b) for a and b vectors in the plane is a modification 
    of the two-dimensional dot product in which a is replaced by the perpendicular vector
    rotated 90 degrees (counterclockwise in standard Euclidean coordinates, clockwise in computer graphics coordinates).
    http://mathworld.wolfram.com/PerpDotProduct.html
    """
    def perpendicularDotProduct(self, anotherVector):
        if self.z != 0 or anotherVector.z != 0:
            raise NotImplementedError("Perpendicular dot product for 3D vectors is not implemented.")
        a = self
        b = anotherVector
        theta = a.angleBetween(b)
        return a.x*b.y - a.y*b.x

    def crossProduct(self, anotherVector):
        u = self
        v = anotherVector
        return Vector((u[1]*v[2] - u[2]*v[1],\
                       u[2]*v[0] - u[0]*v[2],\
                       u[0]*v[1] - u[1]*v[0]))

    def norm(self):
        sumOfSquares = 0
        for i in self.coordinates:
            sumOfSquares += i**2
        return math.sqrt(sumOfSquares)

    def angleBetween(self, anotherVector):
        v = self
        w = anotherVector

        normsProduct = v.norm() * w.norm()
        if normsProduct == 0:
            return 0

        cos = v.dotProduct(w) / float(normsProduct)

        # prevent errors caused by floating point rounding
        if cos >= 1.0:
            return 0
        if cos <= -1.0:
            return math.pi

        return math.acos(cos)


    def reflection(self):
        return Vector(self.initialPoint, self.terminalPoint)
    
    def clockwiseRotationBy90Degrees(self):
        if self.z != 0:
            raise NotImplementedError("Rotation over 3D vectors is not implemented.")
        coordinates = (-self.y, self.x)
        terminalPoint = (coordinates[0] + self.initialPoint[0], coordinates[1] + self.initialPoint[1])
        return Vector(terminalPoint, self.initialPoint)

    def counterclockwiseRotationBy90Degrees(self):
        if self.z != 0:
            raise NotImplementedError("Rotation over 3D vectors is not implemented.")
        coordinates = (self.y, -self.x)
        terminalPoint = (coordinates[0] + self.initialPoint[0], coordinates[1] + self.initialPoint[1])
        return Vector(terminalPoint, self.initialPoint)


    def __len__(self):
        return len(self._coordinates)

    def __iter__(self):
        pass

    def __getitem__(self, index):
        return self._coordinates[index]

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self._coordinates == other._coordinates

    def __hash__(self):
        return hash(self._coordinates)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return repr(self._coordinates)

    def __iter__(self):
        return iter(self.coordinates)

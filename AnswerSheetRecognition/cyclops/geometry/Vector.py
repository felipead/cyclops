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

    def innerProduct(self, anotherVector):
        innerProduct = 0
        for (i,j) in zip(self,anotherVector):
            innerProduct += i*j
        return innerProduct

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

        cos = v.innerProduct(w) / float(normsProduct)

        # prevent errors caused by floating point rounding
        if cos >= 1.0:
            return 0
        if cos <= -1.0:
            return math.pi

        return math.acos(cos)


    def get90DegreeClockwiseRotation(self):
        if self.z != 0:
            raise NotImplementedError()
        coordinates = (-self.y, self.x)
        terminalPoint = (coordinates[0] + self.initialPoint[0], coordinates[1] + self.initialPoint[1])
        return Vector(terminalPoint, self.initialPoint)

    def get90DegreeCounterClockwiseRotation(self):
        if self.z != 0:
            raise NotImplementedError()
        coordinates = (self.y, -self.x)
        terminalPoint = (coordinates[0] + self.initialPoint[0], coordinates[1] + self.initialPoint[1])
        return Vector(terminalPoint, self.initialPoint)

    def getReflection(self):
        return Vector(self.initialPoint, self.terminalPoint)

    def __len__(self):
        return len(self._coordinates)

    def __iter__(self):
        pass

    def __getitem__(self, index):
        if index < len(self._coordinates):
            return self._coordinates[index]
        else:
            raise IndexError()

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self._coordinates == other._coordinates

    def __hash__(self):
        return hash(self._coordinates)

    def __str__(self):
        return str(self._coordinates)

    def __iter__(self):
        return iter(self.coordinates)

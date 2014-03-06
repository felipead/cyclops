import math

class Vector:

    def __init__(self, terminalPoint, initialPoint=(0,0)):
        if len(terminalPoint) != 2 or len(initialPoint) != 2:
            raise Exception("Only 2D vectors are supported.")
        self._terminalPoint = tuple(terminalPoint)
        self._initialPoint = tuple(initialPoint)
        self._coordinates = (terminalPoint[0] - initialPoint[0], terminalPoint[1] - initialPoint[1])

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

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
        return self.x * anotherVector.x + self.y * anotherVector.y

    def norm(self):
        return math.sqrt((self.x**2) + (self.y**2))

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
        coordinates = (-self.y, self.x)
        terminalPoint = (coordinates[0] + self.initialPoint[0], coordinates[1] + self.initialPoint[1])
        return Vector(terminalPoint, self.initialPoint)

    def get90DegreeCounterClockwiseRotation(self):
        coordinates = (self.y, -self.x)
        terminalPoint = (coordinates[0] + self.initialPoint[0], coordinates[1] + self.initialPoint[1])
        return Vector(terminalPoint, self.initialPoint)

    def getMirror(self):
        return Vector(self.initialPoint, self.terminalPoint)

    def __len__(self):
        return 2

    def __iter__(self):
        pass

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
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

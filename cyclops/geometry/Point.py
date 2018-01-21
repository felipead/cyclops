# -*- coding: utf-8 -*-

'''
Represents a dimension agnostic point in the Euclidean space.

Points are read-only objects.
'''
class Point(tuple):

    def __new__(cls, coordinates=(0,)):
        return super().__new__(cls, coordinates)

    @property
    def x(self):
        if len(self) > 0:
            return self[0]
        else:
            return 0

    @property
    def y(self):
        if len(self) > 1:
            return self[1]
        else:
            return 0

    @property
    def z(self):
        if len(self) > 2:
            return self[2]
        else:
            return 0

    '''
    Dimension agnostic equality check. For instance:
        Point(1,2) == Point(1,2,0) == Point(1,2,0,0)
    but:
        Point(1,2) != Point(1,2,3) != Point(1,2,3,5)
    .
    '''
    def __eq__(self, other):
        try:
            if len(self) >= len(other):
                biggestDimensionPoint = self
                smallestDimensionPoint = other
            else:
                biggestDimensionPoint = other
                smallestDimensionPoint = self

            for i in range(len(smallestDimensionPoint)):
                if smallestDimensionPoint[i] != biggestDimensionPoint[i]:
                    return False

            for i in range(len(biggestDimensionPoint) - len(smallestDimensionPoint)):
                if biggestDimensionPoint[len(smallestDimensionPoint) + i] != 0:
                    return False

            return True
        except TypeError:
            return False

    def as2dTuple(self):
        return tuple((self[0], self[1]))

    def as3dTuple(self):
        return tuple((self[0], self[1], self[2]))

    def __hash__(self):
        hashCode = 0
        for x in self:
            if x != 0:
                hashCode ^= 5167 * hash(x)
        return 7907 * hashCode

    def __getitem__(self, index):
        if index < len(self):
            return super(Point,self).__getitem__(index)
        else:
            return 0

    def __repr__(self):
        return super(Point,self).__repr__()

    def __str__(self):
        return repr(self)

    def __len__(self):
        originalLength = super(Point,self).__len__()

        length = originalLength
        zeroInARow = True
        for i in reversed(range(originalLength)):
            x = super(Point,self).__getitem__(i)
            if x == 0 and zeroInARow:
                length -= 1
            if x != 0:
                zeroInARow = False

        return length

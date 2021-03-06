# -*- coding: utf-8 -*-

import math

from ..geometry.Point import *


class Vector:
    '''
    A vector is formally defined as an element of a vector space. In the commonly encountered vector
    space R^n (i.e., Euclidean n-space), a vector is given by n coordinates and can be specified as
    (A_1,A_2,...,A_n). Vectors are sometimes referred to by the number of coordinates they have,
    so a 2-dimensional vector (x_1,x_2) is often called a two-vector, an n-dimensional vector is often
    called an n-vector, and so on.

    A vector from a point A to a point B is denoted AB^→, and a vector v may be denoted  v^→, or more
    commonly, v. The point A is often called the 'tail' of the vector, and B is called the vector's
    'head.'

    http://mathworld.wolfram.com/Vector.html

    The vector represented by this class is dimension agnostic, although certain operations are only
    supported for 2D or 3D dimensions.

    Vectors are read-only objects.
    '''

    def __init__(self, head, tail=Point((0,))):
        if not isinstance(head, Point):
            head = Point(head)
        if not isinstance(tail, Point):
            tail = Point(tail)

        self._head = head
        self._tail = tail

        length = len(self._head)
        if len(self._tail) > length:
            length = len(self._tail)

        coordinates = []
        for i in range(length):
            coordinates.append(self._head[i] - self._tail[i])
        self._coordinates = Point(coordinates)

        self._norm = None

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
    def tail(self):
        return self._tail

    @property
    def head(self):
        return self._head

    '''
    The norm of a mathematical object is a quantity that in some (possibly abstract) sense describes
    the length, size, or extent of the object. The norm of a vector X is often represented as ‖X‖ or |X|.
    http://mathworld.wolfram.com/Norm.html
    '''
    @property
    def norm(self):
        if self._norm is None:
            square_sum = 0
            for i in self.coordinates:
                square_sum += i**2
            self._norm = math.sqrt(square_sum)

        return self._norm

    '''
    The dot product can be defined for two vectors X and Y by

        X · Y = ‖X‖ ‖Y‖ cos(θ)

    where θ is the angle between the vectors and ‖X‖ is the norm. It follows immediately that
    X · Y = 0 if X is perpendicular to Y. The dot product therefore has the geometric interpretation
    as the length of the projection of X onto the unit vector Y^^ when the two vectors are placed
    so that their tails coincide.
    http://mathworld.wolfram.com/DotProduct.html
    '''

    def dot_product(self, other):
        dot_product = 0
        for (i, j) in zip(self, other):
            dot_product += i * j
        return dot_product

    '''
    The 'perp dot product' (a^⊥ · b) for a and b vectors in the plane is a modification
    of the two-dimensional dot product in which a is replaced by the perpendicular vector
    rotated 90 degrees (counterclockwise in standard Euclidean coordinates, clockwise
    in computer graphics coordinates).
    http://mathworld.wolfram.com/PerpDotProduct.html
    '''

    def perpendicular_dot_product(self, other):
        if self.z != 0 or other.z != 0:
            raise NotImplementedError('Perpendicular dot product for 3D vectors is not implemented.')
        a = self
        b = other
        theta = a.angle_between(b)
        return a.x * b.y - a.y * b.x

    '''
    In mathematics, the cross product or vector product is a binary operation on two vectors in
    three-dimensional space. It results in a vector which is perpendicular to both and therefore
    normal to the plane containing them.

    The cross product is defined by the formula:

        a x b = ‖a‖ ‖b‖ sin(θ) n

    where θ is the angle between a and b in the plane containing them (hence, it is between 0° and 180°),
    ‖a‖ and ‖b‖ are the magnitudes of vectors a and b, and n is a unit vector perpendicular to the plane
    containing a and b in the direction given by the right-hand rule.
    http://en.wikipedia.org/wiki/Cross_product
    '''

    def cross_product(self, other):
        u = self
        v = other
        return Vector((u[1] * v[2] - u[2] * v[1],
                       u[2] * v[0] - u[0] * v[2],
                       u[0] * v[1] - u[1] * v[0]))

    '''
    Inner (shortest) angle between two vectors. Orientation agnostic.
    '''

    def angle_between(self, other):
        v = self
        w = other

        norms_product = v.norm * w.norm
        if norms_product == 0:
            return 0

        cos = v.dot_product(w) / float(norms_product)

        # prevent errors caused by floating point rounding
        if cos >= 1.0:
            return 0
        if cos <= -1.0:
            return math.pi

        return math.acos(cos)

    '''
    Gets the reflection of this vector. Like in a mirror, the reflection of a vector AB is BA.
    '''

    def reflection(self):
        return Vector(self.tail, self.head)

    '''
    Gets a clockwise rotation of this vector, in radians.
    http://en.wikipedia.org/wiki/Rotation_matrix
    '''

    def clockwise_rotation_by(self, radians):
        return self.counterclockwise_rotation_by(-radians)

    '''
    Gets a counterclockwise rotation of this vector, in radians.
    http://en.wikipedia.org/wiki/Rotation_matrix
    '''

    def counterclockwise_rotation_by(self, radians):
        if self.z != 0:
            raise NotImplementedError('Rotation for 3D vectors is not implemented.')
        x = self.x * math.cos(radians) - self.y * math.sin(radians)
        y = self.x * math.sin(radians) + self.y * math.cos(radians)
        head = (x + self.tail[0], y + self.tail[1])
        return Vector(head, self.tail)

    '''
    Gets a 90˚ counterclockwise rotation of this vector (left turn).
    '''

    def counterclockwise_rotation_by_90_degrees(self):
        if self.z != 0:
            raise NotImplementedError('Rotation for 3D vectors is not implemented.')
        coordinates = (-self.y, self.x)
        head = (coordinates[0] + self.tail[0], coordinates[1] + self.tail[1])
        return Vector(head, self.tail)

    '''
    Gets a 90˚ clockwise rotation of this vector (right turn).
    '''

    def clockwise_rotation_by_90_degrees(self):
        if self.z != 0:
            raise NotImplementedError('Rotation for 3D vectors is not implemented.')
        coordinates = (self.y, -self.x)
        head = (coordinates[0] + self.tail[0], coordinates[1] + self.tail[1])
        return Vector(head, self.tail)

    '''
    Gets a 180˚ orientation agnostic rotation of this vector.
    '''

    def rotation_by_180_degrees(self):
        return self.clockwise_rotation_by_90_degrees().clockwise_rotation_by_90_degrees()

    '''
    True if this vector has a clockwise angular distance from another vector. This
    means that the shortest angular distance that makes this vector parallel to another
    vector is rotating this vector clockwise by an angle between 0˚ and 180˚ (inclusive).
    '''

    def is_clockwise_distance_from(self, other):
        return self.cross_product(other).z <= 0

    '''
    True if this vector has a counterclockwise angular distance from another vector. This
    means that the shortest angular distance that makes this vector parallel to another
    vector is rotating this vector counterclockwise by an angle between 0˚ and 180˚
    (inclusive).
    '''

    def is_counterclockwise_distance_from(self, other):
        return self.cross_product(other).z >= 0

    def multiplied_by_scalar(self, scalar):
        new_head = []
        for i in range(len(self)):
            new_head.append(scalar * self.coordinates[i] + self.tail[i])
        return Vector(new_head, self.tail)

    def __len__(self):
        return len(self._coordinates)

    def __iter__(self):
        return iter(self._coordinates)

    def __getitem__(self, index):
        return self._coordinates[index]

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self._coordinates == other._coordinates

    def __ne__(self, other):
        return not (self.__eq__(other))

    def __hash__(self):
        return hash(self._coordinates)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'Vector' + repr(self._coordinates)

    def __iter__(self):
        return iter(self.coordinates)

    def __reversed__(self):
        return self.reflection()

# -*- coding: utf-8 -*-

from ..util.MathUtil import *

from .Vector import *
from .Point import *


class Polygon:
    '''
    A polygon can be defined as a geometric object 'consisting of a number of points (called vertices)
    and an equal number of line segments (called sides), namely a cyclically ordered set of points in
    a plane, with no three successive points collinear, together with the line segments joining
    consecutive pairs of the points. In other words, a polygon is closed broken line lying in a plane'
    (Coxeter and Greitzer 1967, p. 51).
    http://mathworld.wolfram.com/Polygon.html

    Polygons are read-only objects.
    '''

    def __init__(self, vertexes):
        if len(vertexes) < 3:
            raise Exception('Polygon can not have less than 3 vertexes.')

        points = []
        for vertex in vertexes:
            if not isinstance(vertex, Point):
                vertex = Point(vertex)
            points.append(vertex)
        self._vertexes = tuple(points)

        self._interior_angles = None
        self._sides = None
        self._contour = None
        self._is_convex = None

    @property
    def vertexes(self):
        return self._vertexes

    @property
    def sides(self):
        if self._sides is None:
            n = len(self.vertexes)
            sides = []
            for i in range(n):
                v1 = self.vertexes[i]
                v2 = self.vertexes[(i + 1) % n]
                sides.append((v1, v2))
            self._sides = tuple(sides)

        return self._sides

    @property
    def contour(self):
        '''
        The ordered list of vectors that, when connected, draw this polygon.
        '''
        if self._contour is None:
            contour = []
            for side in self.sides:
                contour.append(Vector(side[1], side[0]))
            self._contour = tuple(contour)

        return self._contour

    @property
    def interior_angles(self):
        '''
        The list of interior angles in the same order as the list of vertexes.
        '''
        if self._interior_angles is None:
            n = len(self.vertexes)
            angles = []
            for i in range(n):
                v1 = self.vertexes[i]
                v2 = self.vertexes[(i - 1) % n]
                v3 = self.vertexes[(i + 1) % n]
                angle = Vector(v1, v2).angle_between(Vector(v1, v3))
                angles.append(angle)
            self._interior_angles = tuple(angles)

        return self._interior_angles

    @property
    def is_convex(self):
        '''
        A planar polygon is convex if it contains all the line segments connecting any pair of its
        points. Thus, for example, a regular pentagon is convex, while an indented pentagon is not.
        A planar polygon that is not convex is said to be a concave polygon.

        The polygon is convex if and only if all turns from one edge vector to the next have the
        same sense. Therefore, a simple polygon is convex iff

            v_i^⊥ · v_(i+1)

        has the same sign for all i, where (a^⊥ · b) denotes the perpendicular dot product.
        http://mathworld.wolfram.com/ConvexPolygon.html
        '''
        if self._is_convex is None:
            contour = self.contour
            n = len(contour)
            previous_sign = None
            for i in range(n):
                v1 = contour[i]
                v2 = contour[(i + 1) % n]
                sign = MathUtil.sign(v1.perpendicular_dot_product(v2))

                if sign == 0:
                    self._is_convex = False
                    break
                if previous_sign is not None:
                    if sign != previous_sign:
                        self._is_convex = False
                        break
                previous_sign = sign
            if self._is_convex is None:
                self._is_convex = True

        return self._is_convex

    def __getitem__(self, index):
        return self._vertexes[index]

    def __len__(self):
        return len(self._vertexes)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'Polygon' + repr(self._vertexes)

    def __hash__(self):
        return hash(self._vertexes)

    def __iter__(self):
        return iter(self._vertexes)

    def __eq__(self, other):
        if not isinstance(other, Polygon):
            return False

        if self.vertexes == other.vertexes:
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

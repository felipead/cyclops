# -*- coding: utf-8 -*-

from ..util.MathUtil import *

from Vector import *
from Point import *

"""
A polygon can be defined as a geometric object "consisting of a number of points (called vertices) 
and an equal number of line segments (called sides), namely a cyclically ordered set of points in
a plane, with no three successive points collinear, together with the line segments joining 
consecutive pairs of the points. In other words, a polygon is closed broken line lying in a plane"
(Coxeter and Greitzer 1967, p. 51).
http://mathworld.wolfram.com/Polygon.html

Polygons are read-only objects.
"""
class Polygon(object):

    def __init__(self, vertexes):
        if len(vertexes) < 3:
            raise Exception("Polygon can not have less than 3 vertexes.")
        
        points = []
        for vertex in vertexes:
            if not isinstance(vertex,Point):
                vertex = Point(vertex)
            points.append(vertex)
        self._vertexes = tuple(points)

        self._interiorAngles = None
        self._sides = None
        self._contour = None
        self._isConvex = None

    @property
    def vertexes(self):
        return self._vertexes

    @property
    def sides(self):
        if self._sides is None:
            n = len(self.vertexes)
            sides = []
            for i in xrange(n):
                v1 = self.vertexes[i]
                v2 = self.vertexes[(i + 1) % n]
                sides.append((v1,v2))
            self._sides = tuple(sides)

        return self._sides

    """
    The ordered list of vectors that, when connected, draw this polygon.
    """
    @property
    def contour(self):
        if self._contour is None:
            contour = []
            for side in self.sides:
                contour.append(Vector(side[1], side[0]))
            self._contour = tuple(contour)
        
        return self._contour

    """
    The list of interior angles in the same order as the list of vertexes.
    """
    @property
    def interiorAngles(self):
        if self._interiorAngles is None:
            n = len(self.vertexes)
            angles = []
            for i in xrange(n):
                v1 = self.vertexes[i]
                v2 = self.vertexes[(i - 1) % n]
                v3 = self.vertexes[(i + 1) % n]
                angle = Vector(v1,v2).angleBetween(Vector(v1,v3))
                angles.append(angle)
            self._interiorAngles = tuple(angles)
        
        return self._interiorAngles

    """
    A planar polygon is convex if it contains all the line segments connecting any pair of its
    points. Thus, for example, a regular pentagon is convex, while an indented pentagon is not.
    A planar polygon that is not convex is said to be a concave polygon.

    The polygon is convex if and only if all turns from one edge vector to the next have the
    same sense. Therefore, a simple polygon is convex iff

        v_i^⊥ · v_(i+1)

    has the same sign for all i, where (a^⊥ · b) denotes the perpendicular dot product.
    http://mathworld.wolfram.com/ConvexPolygon.html
    """
    @property
    def isConvex(self):
        if self._isConvex is None:
            contour = self.contour
            n = len(contour)
            previousSign = None
            for i in xrange(n):
                v1 = contour[i]
                v2 = contour[(i+1) % n]
                sign = MathUtil.sign(v1.perpendicularDotProduct(v2))
                
                if sign == 0:
                    self._isConvex = False
                    break
                if previousSign != None:
                    if sign != previousSign:
                        self._isConvex = False
                        break
                previousSign = sign
            if self._isConvex is None:
                self._isConvex = True

        return self._isConvex

    def __getitem__(self, index):
        return self._vertexes[index]

    def __len__(self):
        return len(self._vertexes)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Polygon" + repr(self._vertexes)

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

    def __ne__(self,other):
        return not self.__eq__(other)
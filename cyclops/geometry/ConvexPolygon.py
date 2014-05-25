# -*- coding: utf-8 -*-

from Polygon import *

"""
A planar polygon is convex if it contains all the line segments connecting any pair of its
points. Thus, for example, a regular pentagon is convex, while an indented pentagon is not.
A planar polygon that is not convex is said to be a concave polygon.
http://mathworld.wolfram.com/ConvexPolygon.html
"""
class ConvexPolygon(Polygon):
    
    def __init__(self, vertexes):
        super(ConvexPolygon, self).__init__(vertexes)
        if not self.isConvex:
            raise Exception("Polygon must be convex.")
        self._isClockwise = None
        self._centroid = None
        self._area = None

    """
    Determine if a polygon is clockwise oriented, i.e., it's vertexes are ordered to form
    a clockwise path along the polygon contour. Since this is a convex polygon, if the polygon
    is not clockwise it must be counterclockwise oriented.
    """
    @property
    def isClockwise(self):
        if self._isClockwise is None:
            contour = self.contour
            # since this polygon is guaranteed to be convex, we can pick (in order) any pair 
            # of vectors from its oriented contour
            v1 = contour[0]
            v2 = contour[1]
            self._isClockwise = v1.isClockwiseDistanceFrom(v2)

        return self._isClockwise

    """
    The centroid or geometric center of a two-dimensional region is, informally, the point at which 
    a cardboard cut-out of the region could be perfectly balanced on the tip of a pencil (assuming
    uniform density and a uniform gravitational field). Formally, the centroid of a plane figure or
    two-dimensional shape is the arithmetic mean ("average") position of all the points in the shape.
    The definition extends to any object in n-dimensional space: its centroid is the mean position 
    of all the points in all of the coordinate directions.
    http://en.wikipedia.org/wiki/Centroid
    """
    @property
    def centroid(self):
        if self._centroid is None:
            xSum = 0
            ySum = 0
            for vertex in self:
                xSum += vertex.x
                ySum += vertex.y
            n = float(len(self))
            self._centroid = Point((xSum/n, ySum/n))

        return self._centroid

    """
    The area of this convex polygon. Always a positive value, regardless of the polygon's orientation.
    http://mathworld.wolfram.com/PolygonArea.html
    """
    @property
    def area(self):
        if self._area is None:
            n = len(self)
            summation = 0
            for i in xrange(n):
                v1 = self[i % n]
                v2 = self[(i+1) % n]
                summation += v1.x * v2.y - v2.x * v1.y
            self._area = summation/float(2)
        return abs(self._area)

    def __eq__(self, other):
        if not isinstance(other,ConvexPolygon):
            return False

        if self.isClockwise == other.isClockwise:
            return self.contour == other.contour
        else:
            for (i,j) in zip(self.contour, reversed(other.contour)):
                if i != j.reflection():
                    return False
            return True

    def __hash__(self):
        hashValue = 0
        for v in self._vertexes:
             hashValue ^= 13 * hash(v)
        return 7193 * hashValue

    def __repr__(self):
        return "ConvexPolygon" + repr(self._vertexes)
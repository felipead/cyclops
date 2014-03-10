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

    """
    Determine if a polygon is clockwise oriented, i.e., it's vertexes are ordered to form
    a clockwise path along the polygon contour. Since this is a convex polygon, if the polygon
    is not clockwise it must be counterclockwise oriented.
    """
    @property
    def isClockwise(self):
        if self._isClockwise == None:

            contour = self.contour
            # since this polygon is guaranteed to be convex, we can pick any pair of vectors
            # from its oriented contour
            v1 = contour[0]
            v2 = contour[1]

            cross = v1.crossProduct(v2)
            if cross.z <= 0:
                self._isClockwise = True
            else:
                self._isClockwise = False

        return self._isClockwise

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
             hashValue ^= hash(v)
        return 7193 * hashValue
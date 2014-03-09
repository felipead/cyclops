# -*- coding: utf-8 -*-

from Polygon import *

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
class ConvexPolygon(Polygon):
    
    def __init__(self, vertexes):
        super(ConvexPolygon, self).__init__(vertexes)
        if not self.isConvex():
            raise Exception("Polygon must be convex.")
# -*- coding: utf-8 -*-

from .Vector import *
from .ConvexPolygon import *
from ..util.MathUtil import *

import math

'''
A quadrilateral, sometimes also known as a tetragon or quadrangle (Johnson 1929, p. 61) is a
four-sided polygon. If not explicitly stated, all four polygon vertices are generally taken to lie
in a plane. (If the points do not lie in a plane, the quadrilateral is called a skew quadrilateral.)
There are three topological types of quadrilaterals (Wenninger 1983, p. 50): convex quadrilaterals,
concave quadrilaterals, and crossed quadrilaterals (or butterflies, or bow-ties).
http://mathworld.wolfram.com/Quadrilateral.html
http://en.wikipedia.org/wiki/Quadrilateral
'''
class ConvexQuadrilateral(ConvexPolygon):

    __90_DEGREES = math.pi/2

    def __init__(self, vertexes):
        super(ConvexQuadrilateral, self).__init__(vertexes)
        if len(vertexes) != 4:
            raise Exception('Quadrilateral must have 4 vertexes.')

        self._largest_side_length = None
        self._shortest_side_length = None
        self._reversed_contour = None
        self._mirrored_vertexes = None

        self._bottom_left_corner = None
        self._top_left_corner = None
        self._bottom_right_corner = None
        self._top_right_corner = None

    @property
    def largest_side_length(self):
        if self._largest_side_length is None:
            self._largest_side_length = self.__find_largest_side_vector().norm
        return self._largest_side_length

    @property
    def shortest_side_length(self):
        if self._shortest_side_length is None:
            self._shortest_side_length = self.__find_shortest_side_vector().norm
        return self._shortest_side_length

    @property
    def bottom_left_corner(self):
        if self._bottom_left_corner is None:
            self.__find_corners()
        return self._bottom_left_corner

    @property
    def bottom_right_corner(self):
        if self._bottom_right_corner is None:
            self.__find_corners()
        return self._bottom_right_corner

    @property
    def top_left_corner(self):
        if self._top_left_corner is None:
            self.__find_corners()
        return self._top_left_corner

    @property
    def top_right_corner(self):
        if self._top_right_corner is None:
            self.__find_corners()
        return self._top_right_corner

    @property
    def mirrored_vertexes(self):
        if self._mirrored_vertexes == None:
            self._mirrored_vertexes = (self._vertexes[0], self._vertexes[3], self._vertexes[2], self._vertexes[1])
        return self._mirrored_vertexes

    @property
    def reversed_contour(self):
        if self._reversed_contour == None:
            (a, b, c, d) = self.contour
            self._reversed_contour = (reversed(d), reversed(c), reversed(b), reversed(a))
        return self._reversed_contour


    def has_right_interior_angles(self):
        return self.has_right_interior_angles_with_relaxation_of(0)

    def has_right_interior_angles_with_relaxation_of(self, radians):
        right_angle = self.__90_DEGREES
        for angle in self.interior_angles:
            if angle < (right_angle - radians) or angle > (right_angle + radians):
                return False
        return True

    def has_equal_sides(self):
        return self.has_equal_sides_with_relaxation_ratio_of(1.0)

    def has_equal_sides_with_relaxation_ratio_of(self, ratio):
        (size1, size2, size3, size4) = map((lambda v : v.norm), self.contour)
        return MathUtil.equal_within_ratio(size1, size2, ratio) and MathUtil.equal_within_ratio(size1, size3, ratio) \
            and MathUtil.equal_within_ratio(size1, size4, ratio)

    '''
    Gets a new quadrilateral rotated clockwise by a certain angle (in radians) along
    this quadrilateral center.
    This method may suffer from floating point precision loss.
    '''
    def clockwise_rotation_by(self, radians):
        return self.counterclockwise_rotation_by(-radians)

    '''
    Gets a new quadrilateral rotated counterclockwise by a certain angle (in radians)
    along this quadrilateral center.
    This method may suffer from floating point precision loss.
    '''
    def counterclockwise_rotation_by(self, radians):
        cos = math.cos(radians)
        sin = math.sin(radians)
        center = self.centroid

        rotated_vertexes = []
        for v in self.vertexes:
            rotated_x = (v.x - center.x) * cos  -  (v.y - center.y) * sin + center.x;
            rotated_y = (v.x - center.x) * sin  +  (v.y - center.y) * cos + center.y;
            rotated_point = Point((rotated_x, rotated_y))
            rotated_vertexes.append(rotated_point)
        return ConvexQuadrilateral(rotated_vertexes)

    '''
    Gets a new quadrilateral rotated 90˚ clockwise along this quadrilateral center.
    This method does not suffer from floating point precision loss.
    '''
    def clockwise_rotation_by_90_degrees(self):
        center = self.centroid
        rotated_vertexes = []
        for v in self.vertexes:
            rotated_x =   (v.y - center.y) + center.x;
            rotated_y = - (v.x - center.x) + center.y;
            rotated_point = Point((rotated_x, rotated_y))
            rotated_vertexes.append(rotated_point)
        return ConvexQuadrilateral(rotated_vertexes)

    '''
    Gets a new quadrilateral rotated 90˚ counterclockwise along this quadrilateral center.
    This method does not suffer from floating point precision loss.
    '''
    def counterclockwise_rotation_by_90_degrees(self):
        center = self.centroid
        rotated_vertexes = []
        for v in self.vertexes:
            rotated_x = - (v.y - center.y) + center.x;
            rotated_y =   (v.x - center.x) + center.y;
            rotated_point = Point((rotated_x, rotated_y))
            rotated_vertexes.append(rotated_point)
        return ConvexQuadrilateral(rotated_vertexes)

    def as_clockwise(self):
        if self.is_clockwise:
            return self
        else:
            return self.mirrored()

    def as_counterclockwise(self):
        if self.is_clockwise:
            return self.mirrored()
        else:
            return self

    def mirrored(self):
        return ConvexQuadrilateral(self.mirrored_vertexes)

    '''
    Scale this quadrilateral uniformly by a percentage scale. Factor is such that:
        1 is 100%
        2 is 200%
        0.5 is 50%
        ...
    '''
    def scaled_by(self, scale):
        if scale <= 0:
            raise Exception('Scale must be greater than zero.')
        center = self.centroid
        new_vertexes = []
        for vertex in self.vertexes:
            scaled = Vector(vertex, center).multiplied_by_scalar(scale)
            new_vertexes.append(scaled.head)
        return ConvexQuadrilateral(new_vertexes)

    '''
    Project this quadrilateral to a square with sides equal to the largest side of this polygon.
    Useful for perspective correction.

    If this quadrilateral is a lozenge or trapezoid representing a deformed square (for instance,
    a square seen from a angular perspective), then the output of this method will be an approximated
    square that best represents the original square.

    If this quadrilateral is a rectangle or another shape not representing a square, then
    the resulting projection will be a deformed rectangle or shape projected over a square, respectively.
    '''
    def project_to_square(self):
        ab = self.__find_largest_side_vector()
        ba = ab.reflection()

        ad = None
        bc = None
        if self.is_clockwise:
            ad = ab.clockwise_rotation_by_90_degrees()
            bc = ba.counterclockwise_rotation_by_90_degrees()
        else:
            ad = ab.counterclockwise_rotation_by_90_degrees()
            bc = ba.clockwise_rotation_by_90_degrees()

        a_index = self.vertexes.index(ab.tail)
        b_index = self.vertexes.index(ab.head)
        c_index = (b_index + 1) % 4
        d_index = (a_index - 1) % 4

        corrected_vertexes = list(self.vertexes)
        corrected_vertexes[c_index] = bc.head
        corrected_vertexes[d_index] = ad.head

        return ConvexQuadrilateral(corrected_vertexes)

    def __find_largest_side_vector(self):
        largest_side = None
        largest_side_length = 0

        for side in self.contour:
            side_length = side.norm
            if side_length > largest_side_length:
                largest_side = side
                largest_side_length = side_length

        return largest_side

    def __find_shortest_side_vector(self):
        shortest_side = None
        shortest_side_length = float('inf')

        for side in self.contour:
            side_length = side.norm
            if side_length < shortest_side_length:
                shortest_side = side
                shortest_side_length = side_length

        return shortest_side

    def __find_corners(self):
        top = []
        bottom = []
        middle = []
        center = self.centroid

        # First we collect the points which are higher, lower and on the same level than the
        #  centroid (y coordinates).
        for vertex in self.vertexes:
            if vertex.y > center.y:
                top.append(vertex)
            elif vertex.y < center.y:
                bottom.append(vertex)
            else:
                middle.append(vertex)

        # If we have middle points then two vertexes and the centroid are connected by
        # a line parallel to the x axis. This happens, for instance, if this quadrilateral
        # is a perfect square rotated exactly 45˚ around the x axis.
        if len(middle) == 2:
            if middle[0].x < middle[1].x:
                top.append(middle[0])
                bottom.append(middle[1])
            else:
                bottom.append(middle[0])
                top.append(middle[1])

        # If this quadrilateral has a vertex that is too far from the others (for instance, a
        # unbalaced trapezoid), then its centroid will be near that vertex. When that happens,
        # the remaining 3 vertexes are so distant from the centroid that we might capture
        # more than two bottom or top points. Here we fix this, moving a possible extra bottom
        # point to the list of top points, and vice versa.
        if len(bottom) == 3:
            p = self.__find_point_with_largest_y(bottom)
            bottom.remove(p)
            top.append(p)
        elif len(top) == 3:
            p = self.__find_point_with_smallest_y(top)
            top.remove(p)
            bottom.append(p)

        # Now that we have determined the top and bottom points, determine which ones
        # belong to the left and which ones belong to the right.
        if top[0].x < top[1].x:
            self._top_left_corner = top[0]
            self._top_right_corner = top[1]
        else:
            self._top_left_corner = top[1]
            self._top_right_corner = top[0]
        if bottom[0].x < bottom[1].x:
            self._bottom_left_corner = bottom[0]
            self._bottom_right_corner = bottom[1]
        else:
            self._bottom_left_corner = bottom[1]
            self._bottom_right_corner = bottom[0]

    @staticmethod
    def __find_point_with_largest_y(points):
        largest = points[0]
        for point in points[1:]:
            if point.y > largest.y:
                largest = point
        return largest

    @staticmethod
    def __find_point_with_smallest_y(points):
        smallest = points[0]
        for point in points[1:]:
            if point.y < smallest.y:
                smallest = point
        return smallest

    def __repr__(self):
        return 'ConvexQuadrilateral' + repr(self._vertexes)

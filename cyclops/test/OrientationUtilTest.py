from unittest import *

from ..geometry.ConvexQuadrilateral import *
from ..util.OrientationUtil import *

class OrientationUtilTest(TestCase):

    def test_should_rotate_clockwise_square_270_degrees_clockwise_if_orientation_corner_is_at_the_bottom_left_corner(self):
        a = (0,0)
        b = (0,5)
        c = (5,5)
        d = (5,0)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 3

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([d,c,b,a])

    def test_should_rotate_clockwise_square_180_degrees_clockwise_if_orientation_corner_is_at_the_top_left_corner(self):
        a = (0,5)
        b = (5,5)
        c = (5,0)
        d = (0,0)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 2

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([c,d,a,b])

    def test_should_rotate_clockwise_square_90_degrees_clockwise_if_orientation_corner_is_at_the_top_right_corner(self):
        a = (5,5)
        b = (5,0)
        c = (0,0)
        d = (0,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 1

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([b,c,d,a])

    def test_should_not_rotate_clockwise_square_if_orientation_corner_is_at_the_bottom_right_corner(self):
        a = (5,0)
        b = (0,0)
        c = (0,5)
        d = (5,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 0

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([a,b,c,d])

    def test_should_rotate_counterclockwise_square_270_degrees_clockwise_if_orientation_corner_is_at_the_bottom_left_corner(self):
        a = (0,0)
        b = (5,0)
        c = (5,5)
        d = (0,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 3

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([b,c,d,a])

    def test_should_rotate_counterclockwise_square_180_degrees_clockwise_if_orientation_corner_is_at_the_top_left_corner(self):
        a = (0,5)
        b = (0,0)
        c = (5,0)
        d = (5,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 2

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([c,d,a,b])

    def test_should_rotate_counterclockwise_square_90_degrees_clockwise_if_orientation_corner_is_at_the_top_right_corner(self):
        a = (5,5)
        b = (0,5)
        c = (0,0)
        d = (5,0)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 1

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([d,a,b,c])

    def test_should_not_rotate_counterclockwise_square_if_orientation_corner_is_at_the_bottom_right_corner(self):
        a = (5,0)
        b = (0,0)
        c = (0,5)
        d = (5,5)
        square = ConvexQuadrilateral([a,b,c,d])
        orientation_corner = a

        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(square, orientation_corner)
        assert n == 0

        oriented_square = OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(square, n)
        assert oriented_square == ConvexQuadrilateral([a,b,c,d])

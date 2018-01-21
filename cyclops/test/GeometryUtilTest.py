from unittest import *

from ..geometry.Vector import *
from ..geometry.ConvexQuadrilateral import *
from ..util.GeometryUtil import *

class GeometryUtilTest(TestCase):

    def test_create_square_counterclockwise_from_bottom_to_top_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(bottom_left, bottom_right)
        assert square == ConvexQuadrilateral([bottom_left, bottom_right, top_right, top_left])

    def test_create_square_counterclockwise_from_left_to_right_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(top_left, bottom_left)
        assert square == ConvexQuadrilateral([top_left, bottom_left, bottom_right, top_right])

    def test_create_square_counterclockwise_from_right_to_left_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(bottom_right, top_right)
        assert square == ConvexQuadrilateral([bottom_right, top_right, top_left, bottom_left])

    def test_create_square_counterclockwise_from_top_to_bottom_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(top_right, top_left)
        assert square == ConvexQuadrilateral([top_right, top_left, bottom_left, bottom_right])


    def test_create_square_counterclockwise_from_bottom_to_top_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(bottom_left, bottom_right)
        assert square == ConvexQuadrilateral([bottom_left, bottom_right, top_right, top_left])

    def test_create_square_counterclockwise_from_left_to_right_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(top_left, bottom_left)
        assert square == ConvexQuadrilateral([top_left, bottom_left, bottom_right, top_right])

    def test_create_square_counterclockwise_from_right_to_left_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(bottom_right, top_right)
        assert square == ConvexQuadrilateral([bottom_right, top_right, top_left, bottom_left])

    def test_create_square_counterclockwise_from_top_to_bottom_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_counterclockwise_from_two_points(top_right, top_left)
        assert square == ConvexQuadrilateral([top_right, top_left, bottom_left, bottom_right])

    def test_create_square_clockwise_from_top_to_bottom_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_clockwise_from_two_points(top_left, top_right)
        assert square == ConvexQuadrilateral([top_left, top_right, bottom_right, bottom_left])

    def test_create_square_clockwise_from_left_to_right_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_clockwise_from_two_points(bottom_left, top_left)
        assert square == ConvexQuadrilateral([bottom_left, top_left, top_right, bottom_right])

    def test_create_square_clockwise_from_right_to_left_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_clockwise_from_two_points(top_right, bottom_right)
        assert square == ConvexQuadrilateral([top_right, bottom_right, bottom_left, top_left])

    def test_create_square_clockwise_from_bottom_to_top_using_points_parallel_to_axis(self):
        a = 7.3
        bottom_left = (0,0)
        bottom_right = (a,0)
        top_right = (a,a)
        top_left = (0,a)

        square = GeometryUtil.create_square_clockwise_from_two_points(bottom_right, bottom_left)
        assert square == ConvexQuadrilateral([bottom_right, bottom_left, top_left, top_right])

    def test_create_square_clockwise_from_bottom_to_top_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_clockwise_from_two_points(bottom_right, bottom_left)
        assert square == ConvexQuadrilateral([bottom_right, bottom_left, top_left, top_right])

    def test_create_square_clockwise_from_left_to_right_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_clockwise_from_two_points(bottom_left, top_left)
        assert square == ConvexQuadrilateral([bottom_left, top_left, top_right, bottom_right])

    def test_create_square_clockwise_from_right_to_left_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_clockwise_from_two_points(top_right, bottom_right)
        assert square == ConvexQuadrilateral([top_right, bottom_right, bottom_left, top_left])

    def test_create_square_clockwise_from_top_to_bottom_using_points_not_parallel_to_axis(self):
        a = 2
        bottom_left = (0,a)
        bottom_right = (a,0)
        top_right = (2*a,a)
        top_left = (a,2*a)

        square = GeometryUtil.create_square_clockwise_from_two_points(top_left, top_right)
        assert square == ConvexQuadrilateral([top_left, top_right, bottom_right, bottom_left])

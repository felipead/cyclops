from ..geometry.ConvexQuadrilateral import *
from ..geometry.Vector import *
from ..util.MathUtil import *

from unittest import *
import math

class ConvexQuadrilateralTest(TestCase):

    def test_create_convex_quadrilateral(self):
        v1 = (0,0)
        v2 = (0,15)
        v3 = (15,15)
        v4 = (15,0)
        quadrilateral = ConvexQuadrilateral([v1,v2,v3,v4])
        assert quadrilateral.is_convex

    def test_can_not_create_non_convex_quadrilateral(self):
        v1 = (0,0)
        v2 = (3,6)
        v3 = (0,6)
        v4 = (4,2)

        exception_thrown = False
        try:
            ConvexQuadrilateral((v1, v2, v3, v4))
        except:
            exception_thrown = True

        assert exception_thrown

    def test_can_not_create_quadrilateral_with_more_than_4_vertexes(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)
        v4 = (2,5)
        v5 = (0,3)

        exception_thrown = False
        try:
            ConvexQuadrilateral((v1, v2, v3, v4, v5))
        except:
            exception_thrown = True

        assert exception_thrown

    def test_can_not_create_quadrilateral_with_less_than_4_vertexes(self):
        v1 = (0,0)
        v2 = (4,0)
        v3 = (4,3)

        exception_thrown = False
        try:
            ConvexQuadrilateral((v1, v2, v3))
        except:
            exception_thrown = True

        assert exception_thrown

    def test_exact_square_has_right_interior_angles(self):
        square = ConvexQuadrilateral([(0,0), (5,0), (5,5), (0,5)])
        assert square.has_right_interior_angles()

    def test_exact_rectangle_has_right_interior_angles(self):
        rectangle = ConvexQuadrilateral([(0,0), (10,0), (10,5), (0,5)])
        assert rectangle.has_right_interior_angles()

    def test_rough_square_has_rouglhy_right_interior_angles(self):
        d = 0.3
        rough_square = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert rough_square.has_right_interior_angles_with_relaxation_of(0.2)

    def test_too_rough_square_does_not_have_rouglhy_right_interior_angles(self):
        d = 0.7
        too_rough_square = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert not too_rough_square.has_right_interior_angles_with_relaxation_of(0.2)

    def test_trapezoid_does_not_have_roughly_right_interior_angles(self):
        trapezoid = ConvexQuadrilateral([(1,-2), (13,4), (6,8), (-2,4)])
        assert not trapezoid.has_right_interior_angles_with_relaxation_of(0.5)


    def test_exact_square_has_equal_sides(self):
        square = ConvexQuadrilateral([(0,0), (5,0), (5,5), (0,5)])
        assert square.has_equal_sides()

    def test_exact_equilateral_lozenge_has_equal_sides(self):
        lozenge = ConvexQuadrilateral([(0,0), (2,-1), (4,0), (2,1)])
        assert lozenge.has_equal_sides()

    def test_rough_square_has_roughly_equal_sides(self):
        d = 0.3
        rough_square = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert rough_square.has_equal_sides_with_relaxation_ratio_of(1.15)

    def test_too_rough_square_does_not_have_roughly_equal_sides(self):
        d = 2
        too_rough_square = ConvexQuadrilateral([(0,d), (5+d,0), (5+d,5-d), (0-d,5+d)])
        assert not too_rough_square.has_equal_sides_with_relaxation_ratio_of(1.15)

    def test_exact_rectangle_does_not_have_equal_sides(self):
        rectangle = ConvexQuadrilateral([(0,0), (7,0), (7,5), (0,5)])
        assert not rectangle.has_equal_sides()
        assert not rectangle.has_equal_sides_with_relaxation_ratio_of(1.15)

    def test_trapezoid_does_not_have_roughly_equal_sides(self):
        trapezoid = ConvexQuadrilateral([(1,-2), (13,4), (6,8), (-2,4)])
        assert not trapezoid.has_equal_sides_with_relaxation_ratio_of(1.15)

    def test_reversed_contour_of_clockwise_quadrilateral(self):
        a = (0,0)
        b = (0,1)
        c = (1,1)
        d = (1,0)
        square = ConvexQuadrilateral([a,b,c,d])
        reversed_contour = square.reversed_contour

        reversed_vertexes = []
        for v in reversed_contour:
            reversed_vertexes.append(v.tail)

        assert reversed_vertexes == [a,d,c,b]

    def test_reversed_contour_of_counterclockwise_quadrilateral(self):
        a = (0,0)
        b = (1,0)
        c = (1,1)
        d = (0,1)
        square = ConvexQuadrilateral([a,b,c,d])
        reversed_contour = square.reversed_contour

        reversed_vertexes = []
        for v in reversed_contour:
            reversed_vertexes.append(v.tail)

        assert reversed_vertexes == [a,d,c,b]


    def test_rotate_counterclockwise_square_90_degrees_counterclockwise_without_precision_loss(self):
        v1 = (0,2.5)
        v2 = (2.5,0)
        v3 = (5,2.5)
        v4 = (2.5,5)

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        rotated = square.counterclockwise_rotation_by_90_degrees()

        assert rotated[0] == v2
        assert rotated[1] == v3
        assert rotated[2] == v4
        assert rotated[3] == v1

    def test_rotate_counterclockwise_square_90_degrees_clockwise_without_precision_loss(self):
        v1 = (0,2.5)
        v2 = (2.5,0)
        v3 = (5,2.5)
        v4 = (2.5,5)

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        rotated = square.clockwise_rotation_by_90_degrees()

        assert rotated[0] == v4
        assert rotated[1] == v1
        assert rotated[2] == v2
        assert rotated[3] == v3

    def test_rotate_clockwise_square90_degrees_counterclockwise_without_precision_loss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        rotated = square.counterclockwise_rotation_by_90_degrees()

        assert rotated[0] == v4
        assert rotated[1] == v1
        assert rotated[2] == v2
        assert rotated[3] == v3

    def test_rotate_clockwise_square_90_degrees_clockwise_without_precision_loss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)

        square = ConvexQuadrilateral([v1, v2, v3, v4])

        rotated = square.clockwise_rotation_by_90_degrees()
        assert rotated[0] == v2
        assert rotated[1] == v3
        assert rotated[2] == v4
        assert rotated[3] == v1

    def test360_degree_rotation_can_be_achieved_with_four_90_degree_clockwise_rotations_without_precision_loss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        rotated = square.clockwise_rotation_by_90_degrees()
        rotated = rotated.clockwise_rotation_by_90_degrees()
        rotated = rotated.clockwise_rotation_by_90_degrees()
        rotated = rotated.clockwise_rotation_by_90_degrees()
        assert rotated == square

    def test360_degree_rotation_can_be_achieved_with_four_90_degree_counterclockwise_rotations_without_precision_loss(self):
        v1 = (0,2.5)
        v2 = (2.5,5)
        v3 = (5,2.5)
        v4 = (2.5,0)

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        rotated = square.counterclockwise_rotation_by_90_degrees()
        rotated = rotated.counterclockwise_rotation_by_90_degrees()
        rotated = rotated.counterclockwise_rotation_by_90_degrees()
        rotated = rotated.counterclockwise_rotation_by_90_degrees()
        assert rotated == square

    def test_rotate_90_degrees_clockwise_with_precision_loss(self):
        radians = math.pi/2
        error = 0.000000001
        v1 = Point((0,2.5))
        v2 = Point((2.5,0))
        v3 = Point((5,2.5))
        v4 = Point((2.5,5))

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        rotated = square.clockwise_rotation_by(radians)

        assert MathUtil.equal_within_error(rotated[0].x, v4.x, error)
        assert MathUtil.equal_within_error(rotated[0].y, v4.y, error)
        assert MathUtil.equal_within_error(rotated[1].x, v1.x, error)
        assert MathUtil.equal_within_error(rotated[1].y, v1.y, error)
        assert MathUtil.equal_within_error(rotated[2].x, v2.x, error)
        assert MathUtil.equal_within_error(rotated[2].y, v2.y, error)
        assert MathUtil.equal_within_error(rotated[3].x, v3.x, error)
        assert MathUtil.equal_within_error(rotated[3].y, v3.y, error)

    def test_rotate_counterclockwise_square_45_degrees_clockwise_with_precision_loss(self):
        radians = math.pi/4
        error = 0.00001

        side = 5
        v1 = Point((0,0))
        v2 = Point((side,0))
        v3 = Point((side,side))
        v4 = Point((0,side))

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        assert not square.is_clockwise
        rotated = square.clockwise_rotation_by(radians)

        for (original_side,rotated_side) in zip(square.contour,rotated.contour):
            assert MathUtil.equal_within_error(original_side.angle_between(rotated_side), radians, error)
            assert original_side.is_clockwise_distance_from(rotated_side)

    def test_rotate_clockwise_square_45_degrees_clockwise_with_precision_loss(self):
        radians = math.pi/4
        error = 0.000000001

        side = 5
        v1 = Point((0,0))
        v2 = Point((0,side))
        v3 = Point((side,side))
        v4 = Point((side,0))

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        assert square.is_clockwise
        rotated = square.clockwise_rotation_by(radians)

        for (original_side,rotated_side) in zip(square.contour,rotated.contour):
            assert MathUtil.equal_within_error(original_side.angle_between(rotated_side), radians, error)
            assert original_side.is_clockwise_distance_from(rotated_side)

    def test_rotate_90_degrees_counterclockwise_with_precision_loss(self):
        radians = math.pi/2
        error = 0.0000000001
        v1 = Point((0,2.5))
        v2 = Point((2.5,0))
        v3 = Point((5,2.5))
        v4 = Point((2.5,5))

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        rotated = square.counterclockwise_rotation_by(radians)

        assert MathUtil.equal_within_error(rotated[0].x, v2.x, error)
        assert MathUtil.equal_within_error(rotated[0].y, v2.y, error)
        assert MathUtil.equal_within_error(rotated[1].x, v3.x, error)
        assert MathUtil.equal_within_error(rotated[1].y, v3.y, error)
        assert MathUtil.equal_within_error(rotated[2].x, v4.x, error)
        assert MathUtil.equal_within_error(rotated[2].y, v4.y, error)
        assert MathUtil.equal_within_error(rotated[3].x, v1.x, error)
        assert MathUtil.equal_within_error(rotated[3].y, v1.y, error)

    def test_rotate_counterclockwise_square_45_degrees_counterclockwise_with_precision_loss(self):
        radians = math.pi/4
        error = 0.000000001

        side = 5
        v1 = Point((0,0))
        v2 = Point((side,0))
        v3 = Point((side,side))
        v4 = Point((0,side))

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        assert not square.is_clockwise
        rotated = square.counterclockwise_rotation_by(radians)

        for (original_side,rotated_side) in zip(square.contour,rotated.contour):
            assert MathUtil.equal_within_error(original_side.angle_between(rotated_side), radians, error)
            assert not original_side.is_clockwise_distance_from(rotated_side)

    def test_rotate_clockwise_square_45_degrees_counterclockwise_with_precision_loss(self):
        radians = math.pi/4
        error = 0.00001

        side = 5
        v1 = Point((0,0))
        v2 = Point((0,side))
        v3 = Point((side,side))
        v4 = Point((side,0))

        square = ConvexQuadrilateral([v1, v2, v3, v4])
        assert square.is_clockwise
        rotated = square.counterclockwise_rotation_by(radians)

        for (original_side,rotated_side) in zip(square.contour,rotated.contour):
            assert MathUtil.equal_within_error(original_side.angle_between(rotated_side), radians, error)
            assert not original_side.is_clockwise_distance_from(rotated_side)

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_first_point_using_counterclockwise_orientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largest_side = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([a,b,c,d])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == a
        assert square[1] == b
        assert square[2] == new_c
        assert square[3] == new_d
        assert square.is_clockwise == trapezoid.is_clockwise == False

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_second_point_using_counterclockwise_orientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largest_side = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([d,a,b,c])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == new_d
        assert square[1] == a
        assert square[2] == b
        assert square[3] == new_c
        assert square.is_clockwise == trapezoid.is_clockwise == False

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_third_point_using_counterclockwise_orientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largest_side = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([c,d,a,b])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == new_c
        assert square[1] == new_d
        assert square[2] == a
        assert square[3] == b
        assert square.is_clockwise == trapezoid.is_clockwise == False

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_fourth_point_using_counterclockwise_orientation(self):
        b = (6,6)
        c = (4,1)
        d = (7,-4)
        a = (12,0)
        largest_side = Vector(a,b)
        new_c = (0,0)
        new_d = (6,-6)

        trapezoid = ConvexQuadrilateral([b,c,d,a])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == b
        assert square[1] == new_c
        assert square[2] == new_d
        assert square[3] == a
        assert square.is_clockwise == trapezoid.is_clockwise == False

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_fourth_point_using_clockwise_orientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largest_side = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([d,c,b,a])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == new_d
        assert square[1] == new_c
        assert square[2] == b
        assert square[3] == a
        assert square.is_clockwise == trapezoid.is_clockwise == True

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_third_point_using_clockwise_orientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largest_side = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([c,b,a,d])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == new_c
        assert square[1] == b
        assert square[2] == a
        assert square[3] == new_d
        assert square.is_clockwise == trapezoid.is_clockwise == True

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_second_point_using_clockwise_orientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largest_side = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([b,a,d,c])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == b
        assert square[1] == a
        assert square[2] == new_d
        assert square[3] == new_c
        assert square.is_clockwise == trapezoid.is_clockwise == True

    def test_project_to_square_trapezoid_with_largest_side_starting_on_the_second_point_using_clockwise_orientation(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        largest_side = Vector(a,b)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([a,d,c,b])
        square = trapezoid.project_to_square()
        assert square.largest_side_length == largest_side.norm
        assert square[0] == a
        assert square[1] == new_d
        assert square[2] == new_c
        assert square[3] == b
        assert square.is_clockwise == trapezoid.is_clockwise == True

    def test_square_projections_of_quadrilateral_and_its_mirror_are_equal(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        new_c = (12,0)
        new_d = (6,6)

        trapezoid = ConvexQuadrilateral([a,b,c,d])
        square = trapezoid.project_to_square()
        mirrored_trapezoid = ConvexQuadrilateral([a,d,c,b])
        mirrored_square = mirrored_trapezoid.project_to_square()
        assert mirrored_square == square

    def test_square_projection_of_square_is_the_square_itself(self):
        a = (0,0)
        b = (0,5)
        c = (5,5)
        d = (5,0)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.project_to_square() == square


    def test_square_length(self):
        a = 5
        square = ConvexQuadrilateral([(0,a),(a,a),(a,0),(0,0)])
        assert square.largest_side_length == a


    def test_corners_of_aligned_counterclockwise_square(self):
        a = (0,0)
        b = (5,0)
        c = (5,5)
        d = (0,5)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.bottom_left_corner == a
        assert square.bottom_right_corner == b
        assert square.top_right_corner == c
        assert square.top_left_corner == d

    def test_corners_of_aligned_clockwise_square(self):
        a = (0,0)
        b = (5,0)
        c = (5,5)
        d = (0,5)
        square = ConvexQuadrilateral([a,d,c,b])

        assert square.bottom_left_corner == a
        assert square.bottom_right_corner == b
        assert square.top_right_corner == c
        assert square.top_left_corner == d

    def test_corners_of_misaligned_counterclockwise_square(self):
        a = (6,6)
        b = (8,3)
        c = (11,5)
        d = (9,8)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_misaligned_clockwise_square(self):
        a = (6,6)
        b = (8,3)
        c = (11,5)
        d = (9,8)
        square = ConvexQuadrilateral([a,d,c,b])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_counterclockwise_square_with_top_left_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([a,b,c,d])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_clockwise_square_with_top_left_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([a,d,c,b])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_counterclockwise_square_with_top_right_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([d,a,b,c])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_clockwise_square_with_top_right_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([d,c,b,a])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_counterclockwise_square_with_bottom_right_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([c,d,a,b])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_clockwise_square_with_bottom_right_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([c,b,a,d])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_counterclockwise_square_with_bottom_left_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([b,c,d,a])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_45_degrees_inclinated_clockwise_square_with_bottom_left_as_first_vertex(self):
        a = (0,0)
        b = (2,-2)
        c = (4,0)
        d = (2,2)
        square = ConvexQuadrilateral([b,a,d,c])

        assert square.top_left_corner == a
        assert square.bottom_left_corner == b
        assert square.bottom_right_corner == c
        assert square.top_right_corner == d

    def test_corners_of_counterclockwise_trapezoid_with_top_left_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([a,b,c,d])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_clockwise_trapezoid_with_top_left_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([a,d,c,b])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_counterclockwise_trapezoid_with_top_right_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([d,a,b,c])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_clockwise_trapezoid_with_top_right_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([d,c,b,a])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_counterclockwise_trapezoid_with_bottom_right_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([c,d,a,b])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_clockwise_trapezoid_with_bottom_right_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([c,b,a,d])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_counterclockwise_trapezoid_with_bottom_left_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([b,c,d,a])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_clockwise_trapezoid_with_bottom_left_as_first_vertex(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        trapezoid = ConvexQuadrilateral([b,a,d,c])

        assert trapezoid.top_left_corner == a
        assert trapezoid.bottom_left_corner == b
        assert trapezoid.bottom_right_corner == c
        assert trapezoid.top_right_corner == d

    def test_corners_of_counterclockwise_quadrilateral_with_three_vertexes_matching_square_projection(self):
        a = (0,0)
        b = (4,0)
        c = (4,3)
        d = (2,2)
        trapezoid = ConvexQuadrilateral([a,b,c,d])

        assert trapezoid.top_left_corner == d
        assert trapezoid.bottom_left_corner == a
        assert trapezoid.bottom_right_corner == b
        assert trapezoid.top_right_corner == c

    def test_corners_of_clockwise_quadrilateral_with_three_vertexes_matching_square_projection(self):
        a = (0,0)
        b = (4,0)
        c = (4,3)
        d = (2,2)
        trapezoid = ConvexQuadrilateral([a,d,c,b])

        assert trapezoid.top_left_corner == d
        assert trapezoid.bottom_left_corner == a
        assert trapezoid.bottom_right_corner == b
        assert trapezoid.top_right_corner == c

    def test_corners_of_clockwise_and_counterclockwise_squares_are_the_same(self):
        a = (6,6)
        b = (8,3)
        c = (11,5)
        d = (9,8)
        counterclockwise = ConvexQuadrilateral([a,b,c,d])
        clockwise = ConvexQuadrilateral([a,d,c,b])

        assert clockwise.bottom_left_corner == counterclockwise.bottom_left_corner
        assert clockwise.top_left_corner == counterclockwise.top_left_corner
        assert clockwise.bottom_right_corner == counterclockwise.bottom_right_corner
        assert clockwise.top_right_corner == counterclockwise.top_right_corner

    def test_corners_of_clockwise_and_counterclockwise_trapezoids_are_the_same(self):
        a = (0,0)
        b = (6,-6)
        c = (8,-1)
        d = (5,2)
        counterclockwise = ConvexQuadrilateral([a,b,c,d])
        clockwise = ConvexQuadrilateral([a,d,c,b])

        assert clockwise.bottom_left_corner == counterclockwise.bottom_left_corner
        assert clockwise.top_left_corner == counterclockwise.top_left_corner
        assert clockwise.bottom_right_corner == counterclockwise.bottom_right_corner
        assert clockwise.top_right_corner == counterclockwise.top_right_corner

    def test_corners_of_random_quadrilateral1(self):
        a = (197, 385)
        b = (345, 239)
        c = (197, 82)
        d = (55, 251)
        quadrilateral = ConvexQuadrilateral([a,b,c,d])

        assert quadrilateral.bottom_left_corner == c
        assert quadrilateral.bottom_right_corner == b
        assert quadrilateral.top_right_corner == a
        assert quadrilateral.top_left_corner == d

        reversed_quadrilateral = ConvexQuadrilateral([a,d,c,b])
        assert reversed_quadrilateral.bottom_left_corner == c
        assert reversed_quadrilateral.bottom_right_corner == b
        assert reversed_quadrilateral.top_right_corner == a
        assert reversed_quadrilateral.top_left_corner == d

    def test_corners_of_random_quadrilateral2(self):
        a = (153, 346)
        b = (203, 98)
        c = (450, 96)
        d = (430, 370)
        quadrilateral = ConvexQuadrilateral([a,b,c,d])

        assert quadrilateral.bottom_left_corner == b
        assert quadrilateral.bottom_right_corner == c
        assert quadrilateral.top_right_corner == d
        assert quadrilateral.top_left_corner == a

        reversed_quadrilateral = ConvexQuadrilateral([a,d,c,b])
        assert reversed_quadrilateral.bottom_left_corner == b
        assert reversed_quadrilateral.bottom_right_corner == c
        assert reversed_quadrilateral.top_right_corner == d
        assert reversed_quadrilateral.top_left_corner == a

    def test_scale_square_by_200_percent(self):
        scale_factor = 2
        square = ConvexQuadrilateral([(0, 0), (2, 0), (2, 2), (0, 2)])

        scaled = square.scaled_by(scale_factor)
        assert scaled == ConvexQuadrilateral([(-1,-1), (3,-1), (3,3), (-1,3)])

    def test_scale_square_by_150_percent(self):
        scale_factor = 1.5
        square = ConvexQuadrilateral([(0, 0), (2, 0), (2, 2), (0, 2)])

        scaled = square.scaled_by(scale_factor)
        assert scaled == ConvexQuadrilateral([(-0.5,-0.5), (2.5,-0.5), (2.5,2.5), (-0.5,2.5)])

    def test_scale_square_by_100_percent(self):
        scale_factor = 1
        square = ConvexQuadrilateral([(0, 0), (2, 0), (2, 2), (0, 2)])

        scaled = square.scaled_by(scale_factor)
        assert scaled == square

    def test_scale_square_by_50_percent(self):
        scale_factor = 0.5
        square = ConvexQuadrilateral([(0, 0), (4, 0), (4, 4), (0, 4)])

        scaled = square.scaled_by(scale_factor)
        assert scaled == ConvexQuadrilateral([(1,1), (1,3), (3,3), (3,1)])

    def test_scale_lozenge_by_200_percent(self):
        scale_factor = 2
        lozenge = ConvexQuadrilateral([(-2,0),(0,-1),(2,0),(0,1)])
        scaled = lozenge.scaled_by(scale_factor)
        assert scaled == ConvexQuadrilateral([(-4,0),(0,-2),(4,0),(0,2)])

    def test_scale_lozenge_by_25_percent(self):
        scale_factor = 0.25
        lozenge = ConvexQuadrilateral([(-4,0),(0,-2),(4,0),(0,2)])
        scaled = lozenge.scaled_by(scale_factor)
        assert scaled == ConvexQuadrilateral([(-1,0),(0,-0.5),(1,0),(0,0.5)])

    def test_can_not_scale_quadrilateral_by_zero(self):
        scale_factor = 0
        square = ConvexQuadrilateral([(0, 0), (4, 0), (4, 4), (0, 4)])

        exception_thrown = False
        try:
            scaled = square.scaled_by(scale_factor)
        except Exception:
            exception_thrown = True

        assert exception_thrown

    def test_can_not_scale_quadrilateral_by_negative_value(self):
        scale_factor = -1
        square = ConvexQuadrilateral([(0, 0), (4, 0), (4, 4), (0, 4)])

        exception_thrown = False
        try:
            scaled = square.scaled_by(scale_factor)
        except Exception:
            exception_thrown = True

        assert exception_thrown


    def test_clockwise_as_clockwise(self):
        a = (0,0)
        b = (0,4)
        c = (4,4)
        d = (4,0)
        quadrilateral = ConvexQuadrilateral([a, b, c, d])
        clockwise = quadrilateral.as_clockwise()
        assert clockwise[0] == a
        assert clockwise[1] == b
        assert clockwise[2] == c
        assert clockwise[3] == d

    def test_counterclockwise_as_clockwise(self):
        a = (0,0)
        b = (4,0)
        c = (4,4)
        d = (0,4)
        quadrilateral = ConvexQuadrilateral([a, b, c, d])
        clockwise = quadrilateral.as_clockwise()
        assert clockwise[0] == a
        assert clockwise[1] == d
        assert clockwise[2] == c
        assert clockwise[3] == b

    def test_clockwise_as_counterclockwise(self):
        a = (0,0)
        b = (0,4)
        c = (4,4)
        d = (4,0)
        quadrilateral = ConvexQuadrilateral([a, b, c, d])
        counterclockwise = quadrilateral.as_counterclockwise()
        assert counterclockwise[0] == a
        assert counterclockwise[1] == d
        assert counterclockwise[2] == c
        assert counterclockwise[3] == b

    def test_counterclockwise_as_counterclockwise(self):
        a = (0,0)
        b = (4,0)
        c = (4,4)
        d = (0,4)
        quadrilateral = ConvexQuadrilateral([a, b, c, d])
        counterclockwise = quadrilateral.as_counterclockwise()
        assert counterclockwise[0] == a
        assert counterclockwise[1] == b
        assert counterclockwise[2] == c
        assert counterclockwise[3] == d

from ..geometry.Vector import *

from ..geometry.ConvexQuadrilateral import *


class GeometryUtil:

    @staticmethod
    def create_square_clockwise_from_two_points(point1, point2):

        top_right_to_top_left = Vector(point1, point2)

        top_right_to_bottom_right = top_right_to_top_left.counterclockwise_rotation_by_90_degrees()
        top_left_to_bottom_left = reversed(top_right_to_top_left).clockwise_rotation_by_90_degrees()

        bottom_left = top_left_to_bottom_left.head
        top_left = top_left_to_bottom_left.tail
        bottom_right = top_right_to_bottom_right.head
        top_right = top_right_to_bottom_right.tail

        return ConvexQuadrilateral((top_left, top_right, bottom_right, bottom_left))

    @staticmethod
    def create_square_counterclockwise_from_two_points(point1, point2):

        bottom_right_to_bottom_left = Vector(point1, point2)

        bottom_right_to_top_right = bottom_right_to_bottom_left.clockwise_rotation_by_90_degrees()
        bottom_left_to_top_left = reversed(bottom_right_to_bottom_left).counterclockwise_rotation_by_90_degrees()

        bottom_left = bottom_left_to_top_left.tail
        top_left = bottom_left_to_top_left.head
        bottom_right = bottom_right_to_top_right.tail
        top_right = bottom_right_to_top_right.head

        return ConvexQuadrilateral((bottom_left, bottom_right, top_right, top_left))

    # FIXME: add unit tests
    @staticmethod
    def create_rectangle_from_two_points(left_point, right_point, width_scale_ratio):
        left_to_right = Vector(right_point, left_point)
        right_to_left = reversed(left_to_right)

        top_left = left_to_right.counterclockwise_rotation_by_90_degrees().multiplied_by_scalar(width_scale_ratio).head
        bottom_left = left_to_right.clockwise_rotation_by_90_degrees().multiplied_by_scalar(width_scale_ratio).head

        top_right = right_to_left.clockwise_rotation_by_90_degrees().multiplied_by_scalar(width_scale_ratio).head
        bottom_right = right_to_left.counterclockwise_rotation_by_90_degrees().multiplied_by_scalar(width_scale_ratio).head

        return ConvexQuadrilateral((top_left, top_right, bottom_right, bottom_left))

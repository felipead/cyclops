class OrientationUtil:

    @staticmethod
    def find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(quadrilateral, bottom_right_corner):
        if quadrilateral.bottom_left_corner == bottom_right_corner:
            return 3
        elif quadrilateral.top_left_corner == bottom_right_corner:
            return 2
        elif quadrilateral.top_right_corner == bottom_right_corner:
            return 1
        elif quadrilateral.bottom_right_corner == bottom_right_corner:
            return 0
        else:
            raise Exception()

    @staticmethod
    def rotate_quadrilateral_clockwise_by_90_degrees(quadrilateral, number_of_times_to_rotate):
        for i in range(number_of_times_to_rotate):
            quadrilateral = quadrilateral.clockwise_rotation_by_90_degrees()
        return quadrilateral

    @staticmethod
    def orient_quadrilateral(quadrilateral, bottom_right_corner):
        n = OrientationUtil.find_number_of_90_degree_clockwise_rotations_to_orient_quadrilateral(quadrilateral, bottom_right_corner)
        return OrientationUtil.rotate_quadrilateral_clockwise_by_90_degrees(quadrilateral, n)

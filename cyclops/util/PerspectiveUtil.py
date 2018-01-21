import cv2
import numpy

from ..geometry.ConvexQuadrilateral import *


class PerspectiveUtil:

    @staticmethod
    def project_quadrilateral_to_square_picture(picture, quadrilateral_to_be_projected, square_to_project):
        size = int(square_to_project.largest_side_length)
        return PerspectiveUtil.project_quadrilateral_to_rectangle_picture(picture, quadrilateral_to_be_projected, square_to_project, size, size)

    @staticmethod
    def project_quadrilateral_to_rectangle_picture(picture, quadrilateral_to_be_projected, rectangle_to_project, width, heigth):
        source_points = numpy.array(PerspectiveUtil.__as_2d_tuples(quadrilateral_to_be_projected), numpy.float32)
        target_points = numpy.array(PerspectiveUtil.__as_2d_tuples(rectangle_to_project), numpy.float32)

        transform_matrix = cv2.getPerspectiveTransform(source_points, target_points)
        return cv2.warpPerspective(picture, transform_matrix, (width, heigth))

    @staticmethod
    def __as_2d_tuples(quadrilateral):
        return [v.as_2d_tuple() for v in quadrilateral.vertexes]

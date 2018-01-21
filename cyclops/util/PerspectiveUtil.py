import cv2 as cv
import numpy as np

from ..geometry.ConvexQuadrilateral import *

class PerspectiveUtil:

    @staticmethod
    def project_quadrilateral_to_square_picture(picture, quadrilateral_to_be_projected, square_to_project):
        size = int(square_to_project.largest_side_length)
        return PerspectiveUtil.project_quadrilateral_to_rectangle_picture(picture, quadrilateral_to_be_projected, square_to_project, size, size)

    @staticmethod
    def project_quadrilateral_to_rectangle_picture(picture, quadrilateral_to_be_projected, rectangle_to_project, width, heigth):
        source_points = np.array(PerspectiveUtil.__as_2d_tuples(quadrilateral_to_be_projected), np.float32)
        target_points = np.array(PerspectiveUtil.__as_2d_tuples(rectangle_to_project), np.float32)

        transform_matrix = cv.getPerspectiveTransform(source_points, target_points)
        return cv.warpPerspective(picture, transform_matrix, (width, heigth))

    @staticmethod
    def __as_2d_tuples(quadrilateral):
        l = []
        for v in quadrilateral.vertexes:
            l.append(v.as_2d_tuple())
        return l

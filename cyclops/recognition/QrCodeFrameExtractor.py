from ..geometry.ConvexQuadrilateral import *
from ..geometry.Vector import *
from ..util.GeometryUtil import *
from ..util.PerspectiveUtil import *

from .Frame import *


class QrCodeFrameExtractor:

    __LEFT_SCALE = 0.33
    __RIGHT_SCALE = 0.11
    __ANSWER_FRAME_QUADRILATERAL_SCALE = 1.15

    def extract(self, answer_frame):
        answer_frame_quadrilateral = answer_frame.original_quadrilateral.scaled_by(self.__ANSWER_FRAME_QUADRILATERAL_SCALE)
        qr_code_quadrilateral = self._extract_qr_code_quadrilateral(answer_frame_quadrilateral)
        qr_code_projection = self._project_quadrilateral_to_square_picture(answer_frame.original_picture, qr_code_quadrilateral)

        frame = Frame()
        frame.original_quadrilateral = qr_code_quadrilateral
        frame.original_picture = answer_frame.original_picture
        frame.projected_picture = qr_code_projection
        return frame

    def _extract_qr_code_quadrilateral(self, answer_frame_quadrilateral):
        answer_frame_quadrilateral = answer_frame_quadrilateral.as_clockwise()

        right = answer_frame_quadrilateral[1]
        left = answer_frame_quadrilateral[2]
        right_to_left = Vector(left, right)

        scaled_left = right_to_left.multiplied_by_scalar(self.__LEFT_SCALE).head
        scaled_right = right_to_left.rotation_by_180_degrees().multiplied_by_scalar(self.__RIGHT_SCALE).head

        qr_code_quadrilateral = GeometryUtil.create_square_clockwise_from_two_points(scaled_left, scaled_right)
        return qr_code_quadrilateral

    @staticmethod
    def _project_quadrilateral_to_square_picture(picture, quadrilateral):
        counterclockwise_quadrilateral = quadrilateral.as_counterclockwise()
        projection_size = int(counterclockwise_quadrilateral.largest_side_length)
        projection_square = ConvexQuadrilateral([(0, projection_size - 1), (0, 0), (projection_size - 1, 0), (projection_size - 1, projection_size - 1)])

        return PerspectiveUtil.project_quadrilateral_to_square_picture(picture, counterclockwise_quadrilateral, projection_square)

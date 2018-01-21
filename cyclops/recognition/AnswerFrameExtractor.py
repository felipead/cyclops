import math

from .AnswerFrameExtractionResult import *
from .Frame import *

from ..pattern.FrameAlignmentPatternMatcher import *
from ..pattern.FrameOrientationPatternMatcher import *

from ..geometry.Vector import *
from ..geometry.ConvexQuadrilateral import *
from ..util.MathUtil import *
from ..util.PerspectiveUtil import *


class AnswerFrameExtractor:

    __ANSWER_SHEET_QUADRILATERAL_SCALE = 1.15

    def __init__(self, size_relaxation_ratio=1.10, angle_relaxation_radians=0.3):
        self._size_relaxation_ratio = size_relaxation_ratio
        self._angle_relaxation_radians = angle_relaxation_radians
        self._frame_alignment_matcher = FrameAlignmentPatternMatcher()
        self._frame_orientation_matcher = FrameOrientationPatternMatcher()

    def extract(self, picture):
        frame_orientation_matches = self._frame_orientation_matcher.match(picture, 1)
        frame_alignment_matches = self._frame_alignment_matcher.match(picture, 3)

        answer_frame_quadrilaterals = self._find_answer_frame_quadrilaterals(frame_orientation_matches, frame_alignment_matches)
        best_answer_frame_quadrilateral = None
        if answer_frame_quadrilaterals != []:
            best_answer_frame_quadrilateral = self._choose_quadrilateral_that_best_resembles_square(answer_frame_quadrilaterals)

        answer_frame = None
        if best_answer_frame_quadrilateral is not None:
            answer_frame = self.__extract_answer_frame(picture, best_answer_frame_quadrilateral)

        return self.__build_result(answer_frame, answer_frame_quadrilaterals, frame_orientation_matches, frame_alignment_matches)

    def __build_result(self, answer_frame, answer_frame_quadrilaterals, frame_orientation_matches, frame_alignment_matches):
        result = AnswerFrameExtractionResult()
        result.frame_orientation_matches = frame_orientation_matches
        result.frame_alignment_matches = frame_alignment_matches
        if answer_frame is not None:
            result.answer_frame = answer_frame
            answer_frame_mismatches = answer_frame_quadrilaterals
            answer_frame_mismatches.remove(answer_frame.original_quadrilateral)
            result.answer_frame_mismatches = answer_frame_mismatches
        return result

    def _find_answer_frame_quadrilaterals(self, frame_orientation_matches, frame_alignment_matches):
        other_points = []
        for frame_alignment_match in frame_alignment_matches:
            other_points.append(frame_alignment_match.center)

        quadrilaterals = set()
        for frame_orientation_match in frame_orientation_matches:
            base_point = frame_orientation_match.center
            quadrilaterals.update(self._find_convex_quadrilaterals_with_roughly_equal_sizes_and_angles(base_point, other_points))

        return list(quadrilaterals)

    def _find_convex_quadrilaterals_with_roughly_equal_sizes_and_angles(self, base_point, other_points):
        convex_quadrilaterals = set()

        for first_point in other_points:
            base_distance = MathUtil.distance_between_points(first_point, base_point)
            for second_point in other_points:
                if second_point == first_point:
                    continue
                if self.__are_distances_roughly_equal(MathUtil.distance_between_points(first_point, second_point), base_distance):
                    for third_point in other_points:
                        if third_point == first_point or third_point == second_point:
                            continue
                        if self.__are_distances_roughly_equal(MathUtil.distance_between_points(second_point, third_point), base_distance):
                            if self.__are_distances_roughly_equal(MathUtil.distance_between_points(third_point, base_point), base_distance):
                                points = (base_point, first_point, second_point, third_point)
                                quadrilateral = self.__get_convex_quadrilateral_with_roughly_right_interior_angles(points)
                                if quadrilateral is not None:
                                    convex_quadrilaterals.add(quadrilateral)

        return convex_quadrilaterals

    def __get_convex_quadrilateral_with_roughly_right_interior_angles(self, points):
        polygon = Polygon(points)
        if polygon.is_convex:
            convex_quadrilateral = ConvexQuadrilateral(polygon.vertexes)
            if convex_quadrilateral.has_right_interior_angles_with_relaxation_of(self._angle_relaxation_radians):
                return convex_quadrilateral
        return None

    def __are_distances_roughly_equal(self, distance1, distance2):
        return MathUtil.equal_within_ratio(distance1, distance2, self._size_relaxation_ratio)

    def _choose_quadrilateral_that_best_resembles_square(self, frames):
        # TODO
        return frames[0]

    def __extract_answer_frame(self, picture, quadrilateral):
        scaled_quadrilateral = quadrilateral.scaled_by(self.__ANSWER_SHEET_QUADRILATERAL_SCALE)
        counterclockwise_quadrilateral = scaled_quadrilateral.as_counterclockwise()

        projection_size = int(counterclockwise_quadrilateral.largest_side_length)
        projection_square = ConvexQuadrilateral([(projection_size - 1, projection_size - 1), (0, projection_size - 1), (0, 0), (projection_size - 1, 0)])

        projected_answer_frame_picture = PerspectiveUtil.project_quadrilateral_to_square_picture(picture, counterclockwise_quadrilateral, projection_square)

        frame = Frame()
        frame.original_quadrilateral = quadrilateral
        frame.scaled_quadrilateral = scaled_quadrilateral
        frame.original_picture = picture
        frame.projected_picture = projected_answer_frame_picture
        return frame

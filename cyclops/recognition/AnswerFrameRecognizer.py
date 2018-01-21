import cv2

from .AnswerFrameRecognitionResult import *
from ..geometry.ConvexQuadrilateral import *
from ..geometry.ConvexPolygon import *
from ..util.DrawingUtil import *
from ..util.PerspectiveUtil import *
from ..util.ImageProcessingUtil import *
from ..util.GeometryUtil import *

class AnswerFrameRecognizer:

    COLUMN_VERTICAL_PADDING_WIDTH_PERCENTAGE = 0.15
    COLUMN_HORIZONTAL_PADDING_HEIGHT_PERCENTAGE = 0.05
    STRIPE_WIDTH_PERCENTAGE_FROM_COLUMN_WIDTH = 0.15

    STRIPE_MARK_CONTOUR_RELAXATION_FACTOR = 0.07

    STRIPE_MARK_MINIMUM_AREA_PERCENTAGE = 0.005
    STRIPE_MARK_MAXIMUM_AREA_PERCENTAGE = 0.08

    STRIPE_MARK_MAXIMUM_DEVIATION_FROM_AVERAGE_X_RATIO = 1.15
    STRIPE_MARK_INTERLAPSING_Y_RATIO = 1.05

    PICTURE_DILATATION_FACTOR = 1
    PICTURE_EROSION_FACTOR = 1
    PICTURE_BILATERAL_FILTER_DIAMETER = 9
    PICTURE_BILATERAL_FILTER_SIGMA_COLOR = 100
    PICTURE_BILATERAL_FILTER_SIGMA_SPACE = 100 * 5

    PICTURE_SIZE = 300

    STRIPE_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_BLOCK_SIZE = 25
    STRIPE_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_CONSTANT_SUBTRACTED_FROM_MEAN = int(25)

    ANSWER_MARK_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_BLOCK_SIZE = 15
    ANSWER_MARK_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_CONSTANT_SUBTRACTED_FROM_MEAN = int(15)


    def __init__(self):
        # FIXME: WORK IN PROGRESS!!!!
        cv2.namedWindow('answerMark1')
        cv2.namedWindow('answerMark2')

    def recognize(self, answer_frame, qr_code_data):
        width = height = self.PICTURE_SIZE

        picture = answer_frame.projected_picture
        picture = ImageProcessingUtil.resize_image(picture, width, height)
        picture = self._filter_noise(picture)

        vertical_padding = int(width * self.COLUMN_VERTICAL_PADDING_WIDTH_PERCENTAGE)
        horizontal_padding = int(height * self.COLUMN_HORIZONTAL_PADDING_HEIGHT_PERCENTAGE)
        half = int(height/2)

        left_column = ConvexQuadrilateral([(horizontal_padding, vertical_padding),\
                                        (half-horizontal_padding, vertical_padding),\
                                        (half-horizontal_padding, height-vertical_padding),\
                                        (horizontal_padding, height-vertical_padding)])

        right_column = ConvexQuadrilateral([(half+horizontal_padding, vertical_padding),\
                                         (width-horizontal_padding, vertical_padding),\
                                         (width-horizontal_padding, height-vertical_padding),
                                         (half+horizontal_padding, height-vertical_padding)])

        self._recognize_column(picture, left_column, qr_code_data, is_left_column=True)
        self._recognize_column(picture, right_column, qr_code_data, is_left_column=False)

        answer_frame.projected_picture = picture


    def _recognize_column(self, picture, column, qr_code_data, is_left_column):
        left_stripe = self._get_left_stripe(column)
        right_strip = self._get_right_stripe(column)

        left_stripe_marks = self._find_stripe_marks(picture, left_stripe, is_left_stripe=True)
        right_stripe_marks = self._find_stripe_marks(picture, right_strip, is_left_stripe=False)

        ##################
        ## FIXME: DEBUG ##
        ##################

        if len(left_stripe_marks) == len(right_stripe_marks) == qr_code_data.number_questions_per_column:

            # FIXME: WORK IN PROGRESS
            left = left_stripe_marks[0].centroid
            right = right_stripe_marks[0].centroid
            offset = Vector(right, left).norm * 0.05
            left_with_offset = (left.x + offset, left.y)
            right_with_offset = (right.x - offset, right.y)
            rectangle = GeometryUtil.create_rectangle_from_two_points(left_with_offset, right_with_offset, 0.07)
            answer_mark_picture = ImageProcessingUtil.extract_rectangle_from_image(picture, rectangle)
            if is_left_column:
                index = 1
            else:
                index = 2
            cv2.imshow('answerMark' + str(index), self._preprocess_answer_mark_picture(answer_mark_picture))
            # END: WORK IN PROGRESS

            for i in range(qr_code_data.number_questions_per_column):
                left_stripe_mark = left_stripe_marks[i]
                right_stripe_mark = right_stripe_marks[i]
                DrawingUtil.draw_line(picture, left_stripe_mark.centroid, right_stripe_mark.centroid, DrawingUtil.COLOR_GREEN)

            DrawingUtil.draw_quadrilateral_lines(picture, left_stripe, DrawingUtil.COLOR_RED, 1)
            DrawingUtil.draw_quadrilateral_lines(picture, right_strip, DrawingUtil.COLOR_RED, 1)
            for mark in left_stripe_marks + right_stripe_marks:
                DrawingUtil.draw_filled_circle(picture, mark.centroid, 4, DrawingUtil.COLOR_RED)


    def _get_left_stripe(self, column):
        bottom = column.bottom_left_corner.y
        left = column.bottom_left_corner.x
        top = column.top_left_corner.y
        width = column.bottom_right_corner.x - left
        right = left + int(width * self.STRIPE_WIDTH_PERCENTAGE_FROM_COLUMN_WIDTH)
        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])


    def _get_right_stripe(self, column):
        bottom = column.bottom_right_corner.y
        right = column.bottom_right_corner.x
        top = column.top_right_corner.y
        width = right - column.bottom_left_corner.x
        left = right - int(width * self.STRIPE_WIDTH_PERCENTAGE_FROM_COLUMN_WIDTH)
        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])


    def _find_stripe_marks(self, picture, stripe, is_left_stripe):
        stripe_picture = ImageProcessingUtil.extract_rectangle_from_image(picture, stripe)
        stripe_picture = self._preprocess_stripe_picture(stripe_picture)

        minimum_stripe_mark_area = stripe.area * self.STRIPE_MARK_MINIMUM_AREA_PERCENTAGE
        maximum_stripe_mark_area = stripe.area * self.STRIPE_MARK_MAXIMUM_AREA_PERCENTAGE
        discovered_stripe_marks = []

        _, contours, _ = cv2.findContours(stripe_picture, \
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE, offset=stripe.bottom_left_corner)

        for contour in contours:
            relaxed_contour = self.STRIPE_MARK_CONTOUR_RELAXATION_FACTOR * cv2.arcLength(contour, True)
            approximated_contour = cv2.approxPolyDP(contour, relaxed_contour, True)

            if cv2.isContourConvex(approximated_contour):
                num_contour_vertexes = len(approximated_contour)

                ##################
                ## FIXME: DEBUG ##
                ##################
                color = None
                if num_contour_vertexes == 3:
                    color = DrawingUtil.COLOR_BLUE
                elif num_contour_vertexes == 4:
                   color = DrawingUtil.COLOR_GREEN
                elif num_contour_vertexes == 5:
                    color = DrawingUtil.COLOR_YELLOW
                else:
                    color = DrawingUtil.COLOR_WHITE
                DrawingUtil.draw_contour(picture, approximated_contour, color)

                if num_contour_vertexes in (3, 4, 5):
                    stripe_mark = self._get_convex_polygon(approximated_contour)
                    if stripe_mark.area >= minimum_stripe_mark_area and stripe_mark.area <= maximum_stripe_mark_area:
                        discovered_stripe_marks.append(stripe_mark)
                    else:
                        ##################
                        ## FIXME: DEBUG ##
                        ##################
                        DrawingUtil.draw_contour(picture, approximated_contour, DrawingUtil.COLOR_RED)

        valid_stripe_marks = self._filter_invalid_stripe_marks(discovered_stripe_marks, is_left_stripe)
        self._sort_stripe_marks_from_top_to_bottom(valid_stripe_marks)

        ##################
        ## FIXME: DEBUG ##
        ##################
        for mark in discovered_stripe_marks:
            if mark not in valid_stripe_marks:
                DrawingUtil.draw_filled_circle(picture, mark.centroid, 4, DrawingUtil.COLOR_WHITE)

        return valid_stripe_marks



    def _filter_invalid_stripe_marks(self, stripe_marks, is_left_stripe):
        if len(stripe_marks) == 0:
            return []

        average_x = self._find_stripe_marks_average_x(stripe_marks)
        stripe_marks = self._filter_stripe_marks_deviant_from_average_x(stripe_marks, average_x, self.STRIPE_MARK_MAXIMUM_DEVIATION_FROM_AVERAGE_X_RATIO)
        stripe_marks = self._filter_stripe_marks_with_interlapsing_y(stripe_marks, is_left_stripe, self.STRIPE_MARK_INTERLAPSING_Y_RATIO)
        return stripe_marks

    @staticmethod
    def _find_stripe_marks_average_x(stripe_marks):
        summation = 0
        for stripe_mark in stripe_marks:
            summation += stripe_mark.centroid.x
        average_x = summation/len(stripe_marks)
        return average_x

    @staticmethod
    def _filter_stripe_marks_deviant_from_average_x(stripe_marks, average_x, maximum_deviation_ratio):
        filtered = []
        for mark in stripe_marks:
            if MathUtil.equal_within_ratio(mark.centroid.x, average_x, maximum_deviation_ratio):
                filtered.append(mark)
        return filtered

    @staticmethod
    def _filter_stripe_marks_with_interlapsing_y(stripe_marks, is_left_stripe, interlapsing_ratio):
        marks_to_remove = []
        for mark1 in stripe_marks:
            for mark2 in stripe_marks:
                if mark1 != mark2:
                    if MathUtil.equal_within_ratio(mark1.centroid.y, mark2.centroid.y, interlapsing_ratio):
                        mark1_is_left_to_mark2 = mark1.centroid.x < mark2.centroid.x
                        if is_left_stripe:
                            if mark1_is_left_to_mark2:
                                marks_to_remove.append(mark2)
                            else:
                                marks_to_remove.append(mark1)
                        else: # right stripe
                            if mark1_is_left_to_mark2:
                                marks_to_remove.append(mark1)
                            else:
                                marks_to_remove.append(mark2)

        filtered_marks = []
        for mark in stripe_marks:
            if not mark in marks_to_remove:
                filtered_marks.append(mark)

        return filtered_marks

    @staticmethod
    def _sort_stripe_marks_from_top_to_bottom(stripe_marks):
        stripe_marks.sort(key=lambda i: i.centroid.y)

    def _filter_noise(self, picture):
        picture = ImageProcessingUtil.apply_bilateral_filter(picture, \
            self.PICTURE_BILATERAL_FILTER_DIAMETER, \
            self.PICTURE_BILATERAL_FILTER_SIGMA_COLOR, \
            self.PICTURE_BILATERAL_FILTER_SIGMA_SPACE)
        picture = ImageProcessingUtil.apply_rectangular_dilatation(picture, self.PICTURE_DILATATION_FACTOR)
        picture = ImageProcessingUtil.apply_rectangular_erosion(picture, self.PICTURE_EROSION_FACTOR)
        return picture

    def _preprocess_stripe_picture(self, picture):
        picture = ImageProcessingUtil.convert_to_inverted_binary_with_gaussian_adaptative_threshold(picture, \
            self.STRIPE_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_BLOCK_SIZE, \
            self.STRIPE_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_CONSTANT_SUBTRACTED_FROM_MEAN)
        return picture

    def _preprocess_answer_mark_picture(self, picture):
        picture = ImageProcessingUtil.convert_to_inverted_binary_with_gaussian_adaptative_threshold(picture, \
            self.ANSWER_MARK_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_BLOCK_SIZE, \
            self.ANSWER_MARK_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_CONSTANT_SUBTRACTED_FROM_MEAN)
        return picture



    @staticmethod
    def _get_convex_polygon(contour):
        vertexes = []
        for element in contour:
            vertexes.append(element[0])
        return ConvexPolygon(vertexes)

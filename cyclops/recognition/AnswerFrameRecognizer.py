from .AnswerFrameRecognitionResult import *

from ..geometry.ConvexQuadrilateral import *
from ..geometry.ConvexPolygon import *
from ..util.DrawingUtil import *
from ..util.PerspectiveUtil import *
from ..util.ImageProcessingUtil import *
from ..util.GeometryUtil import *

import cv2;

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


    def recognize(self, answerFrame, qrCodeData):
        width = height = self.PICTURE_SIZE

        picture = answerFrame.projectedPicture
        picture = ImageProcessingUtil.resizeImage(picture, width, height)
        picture = self._filterNoise(picture)

        verticalPadding = int(width * self.COLUMN_VERTICAL_PADDING_WIDTH_PERCENTAGE)
        horizontalPadding = int(height * self.COLUMN_HORIZONTAL_PADDING_HEIGHT_PERCENTAGE)
        half = int(height/2)

        leftColumn = ConvexQuadrilateral([(horizontalPadding, verticalPadding),\
                                        (half-horizontalPadding, verticalPadding),\
                                        (half-horizontalPadding, height-verticalPadding),\
                                        (horizontalPadding, height-verticalPadding)])

        rightColumn = ConvexQuadrilateral([(half+horizontalPadding, verticalPadding),\
                                         (width-horizontalPadding, verticalPadding),\
                                         (width-horizontalPadding, height-verticalPadding),
                                         (half+horizontalPadding, height-verticalPadding)])

        self._recognizeColumn(picture, leftColumn, qrCodeData, isLeftColumn=True)
        self._recognizeColumn(picture, rightColumn, qrCodeData, isLeftColumn=False)

        answerFrame.projectedPicture = picture


    def _recognizeColumn(self, picture, column, qrCodeData, isLeftColumn):
        leftStripe = self._getLeftStripe(column)
        rightStripe = self._getRightStripe(column)

        leftStripeMarks = self._findStripeMarks(picture, leftStripe, isLeftStripe=True)
        rightStripeMarks = self._findStripeMarks(picture, rightStripe, isLeftStripe=False)

        ##################
        ## FIXME: DEBUG ##
        ##################

        if len(leftStripeMarks) == len(rightStripeMarks) == qrCodeData.numberOfQuestionsPerColumn:

            # FIXME: WORK IN PROGRESS
            left = leftStripeMarks[0].centroid
            right = rightStripeMarks[0].centroid
            offset = Vector(right, left).norm * 0.05
            leftWithOffset = (left.x + offset, left.y)
            rightWithOffset = (right.x - offset, right.y)
            rectangle = GeometryUtil.createRectangleFromTwoPoints(leftWithOffset, rightWithOffset, 0.07)
            answerMarkPicture = ImageProcessingUtil.extractRectangleFromImage(picture, rectangle)
            if isLeftColumn:
                index = 1
            else:
                index = 2
            cv2.imshow('answerMark' + str(index), self._preprocessAnswerMarkPicture(answerMarkPicture))
            # END: WORK IN PROGRESS

            for i in range(qrCodeData.numberOfQuestionsPerColumn):
                leftStripeMark = leftStripeMarks[i]
                rightStripeMark = rightStripeMarks[i]
                DrawingUtil.drawLine(picture, leftStripeMark.centroid, rightStripeMark.centroid, DrawingUtil.COLOR_GREEN)

            DrawingUtil.drawQuadrilateralLines(picture, leftStripe, DrawingUtil.COLOR_RED, 1)
            DrawingUtil.drawQuadrilateralLines(picture, rightStripe, DrawingUtil.COLOR_RED, 1)
            for mark in leftStripeMarks + rightStripeMarks:
                DrawingUtil.drawFilledCircle(picture, mark.centroid, 4, DrawingUtil.COLOR_RED)


    def _getLeftStripe(self, column):
        bottom = column.bottomLeftCorner.y
        left = column.bottomLeftCorner.x
        top = column.topLeftCorner.y
        width = column.bottomRightCorner.x - left
        right = left + int(width * self.STRIPE_WIDTH_PERCENTAGE_FROM_COLUMN_WIDTH)
        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])


    def _getRightStripe(self, column):
        bottom = column.bottomRightCorner.y
        right = column.bottomRightCorner.x
        top = column.topRightCorner.y
        width = right - column.bottomLeftCorner.x
        left = right - int(width * self.STRIPE_WIDTH_PERCENTAGE_FROM_COLUMN_WIDTH)
        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])


    def _findStripeMarks(self, picture, stripe, isLeftStripe):
        stripePicture = ImageProcessingUtil.extractRectangleFromImage(picture, stripe)
        stripePicture = self._preprocessStripePicture(stripePicture)

        minimumStripeMarkArea = stripe.area * self.STRIPE_MARK_MINIMUM_AREA_PERCENTAGE
        maximumStripeMarkArea = stripe.area * self.STRIPE_MARK_MAXIMUM_AREA_PERCENTAGE
        discoveredStripeMarks = []

        _, contours, _ = cv2.findContours(stripePicture, \
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE, offset=stripe.bottomLeftCorner)

        for contour in contours:
            relaxedContour = self.STRIPE_MARK_CONTOUR_RELAXATION_FACTOR * cv2.arcLength(contour, True)
            approximatedContour = cv2.approxPolyDP(contour, relaxedContour, True)

            if cv2.isContourConvex(approximatedContour):
                numberOfContourVertexes = len(approximatedContour)

                ##################
                ## FIXME: DEBUG ##
                ##################
                color = None
                if numberOfContourVertexes == 3:
                    color = DrawingUtil.COLOR_BLUE
                elif numberOfContourVertexes == 4:
                   color = DrawingUtil.COLOR_GREEN
                elif numberOfContourVertexes == 5:
                    color = DrawingUtil.COLOR_YELLOW
                else:
                    color = DrawingUtil.COLOR_WHITE
                DrawingUtil.drawContour(picture, approximatedContour, color)

                if numberOfContourVertexes in (3, 4, 5):
                    stripeMark = self._getConvexPolygon(approximatedContour)
                    if stripeMark.area >= minimumStripeMarkArea and stripeMark.area <= maximumStripeMarkArea:
                        discoveredStripeMarks.append(stripeMark)
                    else:
                        ##################
                        ## FIXME: DEBUG ##
                        ##################
                        DrawingUtil.drawContour(picture, approximatedContour, DrawingUtil.COLOR_RED)

        validStripeMarks = self._filterInvalidStripeMarks(discoveredStripeMarks, isLeftStripe)
        self._sortStripeMarksFromTopToBottom(validStripeMarks)

        ##################
        ## FIXME: DEBUG ##
        ##################
        for mark in discoveredStripeMarks:
            if mark not in validStripeMarks:
                DrawingUtil.drawFilledCircle(picture, mark.centroid, 4, DrawingUtil.COLOR_WHITE)

        return validStripeMarks



    def _filterInvalidStripeMarks(self, stripeMarks, isLeftStripe):
        if len(stripeMarks) == 0:
            return []

        averageX = self._findStripeMarksAverageX(stripeMarks)
        stripeMarks = self._filterStripeMarksDeviantFromAverageX(stripeMarks, averageX, self.STRIPE_MARK_MAXIMUM_DEVIATION_FROM_AVERAGE_X_RATIO)
        stripeMarks = self._filterStripeMarksWithInterlapsingY(stripeMarks, isLeftStripe, self.STRIPE_MARK_INTERLAPSING_Y_RATIO)
        return stripeMarks

    @staticmethod
    def _findStripeMarksAverageX(stripeMarks):
        summation = 0
        for stripeMark in stripeMarks:
            summation += stripeMark.centroid.x
        averageX = summation/len(stripeMarks)
        return averageX

    @staticmethod
    def _filterStripeMarksDeviantFromAverageX(stripeMarks, averageX, maximumDeviationRatio):
        filteredStripeMarks = []
        for mark in stripeMarks:
            if MathUtil.equalWithinRatio(mark.centroid.x, averageX, maximumDeviationRatio):
                filteredStripeMarks.append(mark)
        return filteredStripeMarks

    @staticmethod
    def _filterStripeMarksWithInterlapsingY(stripeMarks, isLeftStripe, interlapsingRatio):
        marksToRemove = []
        for mark1 in stripeMarks:
            for mark2 in stripeMarks:
                if mark1 != mark2:
                    if MathUtil.equalWithinRatio(mark1.centroid.y, mark2.centroid.y, interlapsingRatio):
                        mark1IsLeftToMark2 = mark1.centroid.x < mark2.centroid.x
                        if isLeftStripe:
                            if mark1IsLeftToMark2:
                                marksToRemove.append(mark2)
                            else:
                                marksToRemove.append(mark1)
                        else: # right stripe
                            if mark1IsLeftToMark2:
                                marksToRemove.append(mark1)
                            else:
                                marksToRemove.append(mark2)

        filteredMarks = []
        for mark in stripeMarks:
            if not mark in marksToRemove:
                filteredMarks.append(mark)

        return filteredMarks

    @staticmethod
    def _sortStripeMarksFromTopToBottom(stripeMarks):
        stripeMarks.sort(key=lambda i: i.centroid.y)

    def _filterNoise(self, picture):
        picture = ImageProcessingUtil.applyBilateralFilter(picture, \
            self.PICTURE_BILATERAL_FILTER_DIAMETER, \
            self.PICTURE_BILATERAL_FILTER_SIGMA_COLOR, \
            self.PICTURE_BILATERAL_FILTER_SIGMA_SPACE)
        picture = ImageProcessingUtil.applyRectangularDilatation(picture, self.PICTURE_DILATATION_FACTOR)
        picture = ImageProcessingUtil.applyRectangularErosion(picture, self.PICTURE_EROSION_FACTOR)
        return picture

    def _preprocessStripePicture(self, picture):
        picture = ImageProcessingUtil.convertToInvertedBinaryWithGaussianAdaptativeThreshold(picture, \
            self.STRIPE_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_BLOCK_SIZE, \
            self.STRIPE_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_CONSTANT_SUBTRACTED_FROM_MEAN)
        return picture

    def _preprocessAnswerMarkPicture(self, picture):
        picture = ImageProcessingUtil.convertToInvertedBinaryWithGaussianAdaptativeThreshold(picture, \
            self.ANSWER_MARK_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_BLOCK_SIZE, \
            self.ANSWER_MARK_PICTURE_GUASSIAN_ADAPTATIVE_THRESHOLD_CONSTANT_SUBTRACTED_FROM_MEAN)
        return picture



    @staticmethod
    def _getConvexPolygon(contour):
        vertexes = []
        for element in contour:
            vertexes.append(element[0])
        return ConvexPolygon(vertexes)

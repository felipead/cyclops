from AnswerFrameRecognitionResult import *

from ..geometry.ConvexQuadrilateral import *
from ..geometry.ConvexPolygon import *
from ..util.DrawingUtil import *
from ..util.PerspectiveUtil import *
from ..util.ImageProcessingUtil import *

import cv2;

class AnswerFrameRecognizer:

    VERTICAL_PADDING_WIDTH_PERCENTAGE = 0.15
    HORIZONTAL_PADDING_HEIGHT_PERCENTAGE = 0.05
    STRIPE_WIDTH_PERCENTAGE_FROM_COLUMN_WIDTH = 0.15

    # FIXME: Resolution Dependence
    STRIPE_IMAGE_EROSION_FACTOR = 1
    STRIPE_IMAGE_DILATATION_FACTOR = 1
    STRIPE_MARK_CONTOUR_RELAXATION_FACTOR = 0.07

    STRIPE_MARK_MINIMUM_AREA_PERCENTAGE = 0.005
    STRIPE_MARK_MAXIMUM_AREA_PERCENTAGE = 0.04
    STRIPE_MARK_MAXIMUM_DEVIATION_FROM_STRIPE_LINE_PERCENTAGE = 1.08


    def recognize(self, answerFrame, qrCodeData):
        picture = answerFrame.projectedPicture
        width, height = picture.shape[:2]
        
        verticalPadding = int(height * self.VERTICAL_PADDING_WIDTH_PERCENTAGE)
        horizontalPadding = int(width * self.HORIZONTAL_PADDING_HEIGHT_PERCENTAGE)
        half = int(width/2)

        leftColumn = ConvexQuadrilateral([(horizontalPadding, verticalPadding),\
                                        (half-horizontalPadding, verticalPadding),\
                                        (half-horizontalPadding, height-verticalPadding),\
                                        (horizontalPadding, height-verticalPadding)])

        rightColumn = ConvexQuadrilateral([(half+horizontalPadding, verticalPadding),\
                                         (width-horizontalPadding, verticalPadding),\
                                         (width-horizontalPadding, height-verticalPadding),
                                         (half+horizontalPadding, height-verticalPadding)])

        self._recognizeColumn(picture, leftColumn, qrCodeData)
        self._recognizeColumn(picture, rightColumn, qrCodeData)


    def _recognizeColumn(self, picture, column, qrCodeData):
        leftStripe = self._getLeftStripe(column)
        rightStripe = self._getRightStripe(column)

        leftStripeMarks = self._findStripeMarks(picture, leftStripe)
        rightStripeMarks = self._findStripeMarks(picture, rightStripe)

        ##################
        ## FIXME: DEBUG ##
        ##################
        DrawingUtil.drawQuadrilateralLines(picture, leftStripe, DrawingUtil.COLOR_RED, 1)
        DrawingUtil.drawQuadrilateralLines(picture, rightStripe, DrawingUtil.COLOR_RED, 1)
        for mark in leftStripeMarks + rightStripeMarks:
            DrawingUtil.drawFilledCircle(picture, mark.centroid, 2, DrawingUtil.COLOR_RED)

        if len(leftStripeMarks) == len(rightStripeMarks) == qrCodeData.numberOfQuestionsPerColumn:
            for i in xrange(qrCodeData.numberOfQuestionsPerColumn):
                leftStripeMark = leftStripeMarks[i]
                rightStripeMark = rightStripeMarks[i]
                DrawingUtil.drawLine(picture, leftStripeMark.centroid, rightStripeMark.centroid, DrawingUtil.COLOR_GREEN)
             

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


    def _findStripeMarks(self, picture, stripe):
        stripePicture = ImageProcessingUtil.extractRectangleFromImage(picture, stripe)
        stripePicture = self._preprocessStripePicture(stripePicture)

        minimumStripeMarkArea = stripe.area * self.STRIPE_MARK_MINIMUM_AREA_PERCENTAGE
        maximumStripeMarkArea = stripe.area * self.STRIPE_MARK_MAXIMUM_AREA_PERCENTAGE
        discoveredStripeMarks = []

        contours, _ = cv2.findContours(stripePicture, \
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

        validStripeMarks = self._filterDeviantStripeMarks(discoveredStripeMarks)
        self._sortStripeMarksFromTopToBottom(validStripeMarks)
        return validStripeMarks


    def _preprocessStripePicture(self, stripePicture):
        stripePicture = ImageProcessingUtil.convertToInvertedBinaryWithOptimalThreshold(stripePicture)
        stripePicture = ImageProcessingUtil.applyRectangularErosion(stripePicture, self.STRIPE_IMAGE_EROSION_FACTOR)
        stripePicture = ImageProcessingUtil.applyRectangularDilatation(stripePicture, self.STRIPE_IMAGE_DILATATION_FACTOR)
        return stripePicture


    def _filterDeviantStripeMarks(self, stripeMarks):
        if len(stripeMarks) == 0:
            return []

        summation = 0
        for stripeMark in stripeMarks:
            summation += stripeMark.centroid.x
        averageX = summation/len(stripeMarks)

        filteredStripeMarks = []
        for stripeMark in stripeMarks:
            if MathUtil.equalWithinRatio(stripeMark.centroid.x, averageX, self.STRIPE_MARK_MAXIMUM_DEVIATION_FROM_STRIPE_LINE_PERCENTAGE):
                filteredStripeMarks.append(stripeMark)

        return filteredStripeMarks


    def _sortStripeMarksFromTopToBottom(self, stripeMarks):
        stripeMarks.sort(lambda stripeMark1, stripeMark2: cmp(stripeMark1.centroid.y, stripeMark2.centroid.y))


    @staticmethod
    def _getConvexPolygon(contour):
        vertexes = []
        for element in contour:
            vertexes.append(element[0])
        return ConvexPolygon(vertexes)
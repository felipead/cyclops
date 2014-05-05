from AnswerFrameRecognitionResult import *

from ..geometry.ConvexQuadrilateral import *
from ..util.DrawingUtil import *
from ..util.PerspectiveUtil import *
from ..geometry.ConvexPolygon import *

import cv2;
import cv;

class AnswerFrameRecognizer:

    def recognize(self, answerFrame, numberOfQuestions, numberOfAnswerChoices):
        picture = answerFrame.projectedPicture
        width, height = picture.shape[:2]
        
        # FIXME: MAGIC NUMBERS
        verticalPadding = int(height * 0.15)
        horizontalPadding = int(width * 0.05)
        half = int(width/2)

        leftSide = ConvexQuadrilateral([(horizontalPadding, verticalPadding), (half-horizontalPadding, verticalPadding), (half-horizontalPadding, height-verticalPadding), (horizontalPadding, height-verticalPadding)])
        rightSide = ConvexQuadrilateral([(half+horizontalPadding, verticalPadding), (width-horizontalPadding, verticalPadding), (width-horizontalPadding, height-verticalPadding), (half+horizontalPadding, height-verticalPadding)])

        self._recognizeSide(picture, leftSide)
        self._recognizeSide(picture, rightSide)

        # FIXME
        return None

    def _recognizeSide(self, picture, sideQuadrilateral):
        leftStripeQuadrilateral = self._getLeftStripe(sideQuadrilateral)
        rightStripeQuadrilateral = self._getRightStripe(sideQuadrilateral)

        DrawingUtil.drawQuadrilateralLines(picture, leftStripeQuadrilateral, DrawingUtil.COLOR_RED, 1)
        DrawingUtil.drawQuadrilateralLines(picture, rightStripeQuadrilateral, DrawingUtil.COLOR_RED, 1)

        leftStripeMarks = self._findStripeMarks(picture, leftStripeQuadrilateral)
        rightStripeMarks = self._findStripeMarks(picture, rightStripeQuadrilateral)

        for mark in leftStripeMarks + rightStripeMarks:
            DrawingUtil.drawFilledCircle(picture, mark.centroid, 2, DrawingUtil.COLOR_RED)

        # FIXME: MAGIC NUMBER
        if len(leftStripeMarks) == len(rightStripeMarks) == 10:
            for i in xrange(10):
                leftStripeMark = leftStripeMarks[i]
                rightStripeMark = rightStripeMarks[i]
                DrawingUtil.drawLine(picture, leftStripeMark.centroid, rightStripeMark.centroid, DrawingUtil.COLOR_GREEN)
             

    def _findStripeMarks(self, picture, stripeQuadrilateral):
        stripePicture = self._extractStripePicture(picture, stripeQuadrilateral)
        contours, _ = cv2.findContours(stripePicture, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE, offset=stripeQuadrilateral.bottomLeftCorner)

        stripeArea = stripeQuadrilateral.area
        # FIXME: MAGIC NUMBERS
        minimumArea = stripeArea * 0.006
        maximumArea = stripeArea * 0.020

        stripeMarks = []
        for contour in contours:
            # FIXME: MAGIC NUMBER
            relaxedContour = 0.07 * cv2.arcLength(contour,True)
            approximatedContour = cv2.approxPolyDP(contour, relaxedContour, True)

            if cv2.isContourConvex(approximatedContour):
                stripeMark = self._getConvexPolygon(approximatedContour)
                area = stripeMark.area
                numberOfSides = len(stripeMark)

                if numberOfSides in (3,4,5):
                    if area >= minimumArea and area <= maximumArea:
                        stripeMarks.append(stripeMark)

                color = None
                if numberOfSides == 3:
                    color = DrawingUtil.COLOR_BLUE
                elif numberOfSides == 4:
                   color = DrawingUtil.COLOR_GREEN
                elif numberOfSides == 5:
                    color = DrawingUtil.COLOR_YELLOW
                else:
                    color = DrawingUtil.COLOR_WHITE
                DrawingUtil.drawContour(picture, approximatedContour, color)

        filteredStripeMarks = self._filterDeviantStripeMarks(stripeMarks)
        filteredStripeMarks.sort(lambda mark1, mark2: cmp(mark1.centroid.y, mark2.centroid.y))
        return filteredStripeMarks

    def _filterDeviantStripeMarks(self, stripeMarks):
        if len(stripeMarks) == 0:
            return []

        summation = 0
        for stripeMark in stripeMarks:
            summation += stripeMark.centroid.x
        averageX = summation/len(stripeMarks)
        
        filteredStripeMarks = []
        for stripeMark in stripeMarks:
            # FIXME: MAGIC NUMBER
            if MathUtil.equalWithinRatio(stripeMark.centroid.x, averageX, 1.10):
                filteredStripeMarks.append(stripeMark)

        return filteredStripeMarks

    def _extractStripePicture(self, picture, stripe):
        left = stripe.bottomLeftCorner.x
        right = stripe.bottomRightCorner.x
        bottom = stripe.bottomRightCorner.y
        top = stripe.topRightCorner.y

        width = right - left
        height = top - bottom

        projectedStripe = ConvexQuadrilateral([(0, 0), (width, 0), (width, height), (0, height)])

        picture = PerspectiveUtil.projectQuadrilateralToRectanglePicture(picture, stripe, projectedStripe, width, height)
        return self._binarizeImage(picture)

    def _getLeftStripe(self, quadrilateral):
        bottom = quadrilateral.bottomLeftCorner.y
        left = quadrilateral.bottomLeftCorner.x
        top = quadrilateral.topLeftCorner.y

        width = quadrilateral.bottomRightCorner.x - left
        # FIXME: MAGIC NUMBER
        right = left + int(width * 0.15)

        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])


    def _getRightStripe(self, quadrilateral):
        bottom = quadrilateral.bottomRightCorner.y
        right = quadrilateral.bottomRightCorner.x
        top = quadrilateral.topRightCorner.y

        width = right - quadrilateral.bottomLeftCorner.x
        # FIXME: MAGIC NUMBER
        left = right - int(width * 0.15)

        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])

    @staticmethod
    def _binarizeImage(image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return binary

    @staticmethod
    def _getConvexPolygon(contour):
        vertexes = []
        for element in contour:
            vertexes.append(element[0])
        return ConvexPolygon(vertexes)


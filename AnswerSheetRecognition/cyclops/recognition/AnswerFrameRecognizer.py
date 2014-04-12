from AnswerFrameRecognitionResult import *

from ..geometry.ConvexQuadrilateral import *
from ..util.DrawingUtil import *
from ..util.PerspectiveUtil import *

import cv2;
import cv;

class AnswerFrameRecognizer:

    def __init__(self):
        # FIXME: DEBUG CODE
        cv2.namedWindow("left-left")
        cv2.namedWindow("left-right")
        cv2.namedWindow("right-left")
        cv2.namedWindow("right-right")


    def recognize(self, answerFrame, numberOfQuestions, numberOfAnswerChoices):
        picture = answerFrame.projectedPicture
        width, height = picture.shape[:2]
        
        # FIXME: MAGIC NUMBERS
        verticalPadding = int(height * 0.15)
        horizontalPadding = int(width * 0.03)
        half = int(width/2)

        leftSide = ConvexQuadrilateral([(horizontalPadding, verticalPadding), (half-horizontalPadding, verticalPadding), (half-horizontalPadding, height-verticalPadding), (horizontalPadding, height-verticalPadding)])
        rightSide = ConvexQuadrilateral([(half+horizontalPadding, verticalPadding), (width-horizontalPadding, verticalPadding), (width-horizontalPadding, height-verticalPadding), (half+horizontalPadding, height-verticalPadding)])

        leftLeftStripe = self._getLeftStripe(leftSide)
        leftRightStripe = self._getRightStripe(leftSide)
        leftLeftStripePicture = self._extractStripePicture(picture, leftLeftStripe)
        leftRightStripePicture = self._extractStripePicture(picture, leftRightStripe)
        self._findStripeMarks(leftLeftStripePicture)
        self._findStripeMarks(leftRightStripePicture)
        
        rightLeftStripe = self._getLeftStripe(rightSide)
        rightRightStripe = self._getRightStripe(rightSide)
        rightLeftStripePicture = self._extractStripePicture(picture, rightLeftStripe)
        rightRightStripePicture = self._extractStripePicture(picture, rightRightStripe)
        self._findStripeMarks(rightLeftStripePicture)
        self._findStripeMarks(rightRightStripePicture)

        # FIXME: DEBUG CODE
        cv2.imshow("left-left", leftLeftStripePicture)
        cv2.imshow("left-right", leftRightStripePicture)
        cv2.imshow("right-left", rightLeftStripePicture)
        cv2.imshow("right-right", rightRightStripePicture)

        # FIXME
        return None


    def _findStripeMarks(self, picture):
        gray = cv2.cvtColor(picture, cv.CV_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary, 1, 2)

        for contour in contours:
            relaxedContour = 0.1*cv2.arcLength(contour,True)
            approximatedContour = cv2.approxPolyDP(contour, relaxedContour, True)
            size = len(approximatedContour)
            if cv2.isContourConvex(approximatedContour):
                if size == 3:
                    cv2.drawContours(picture,[contour],0,cv.RGB(0,0,255),-1)
                elif size == 4:
                    cv2.drawContours(picture,[contour],0,cv.RGB(0,255,0),-1)
                elif size == 5:
                    cv2.drawContours(picture,[contour],0,cv.RGB(255,0,0),-1)
                else:
                    cv2.drawContours(picture,[contour],0,cv.RGB(255,0,255),-1)


    def _extractStripePicture(self, picture, stripe):
        left = stripe.bottomLeftCorner.x
        right = stripe.bottomRightCorner.x
        bottom = stripe.bottomRightCorner.y
        top = stripe.topRightCorner.y

        width = right - left
        height = top - bottom

        projectedStripe = ConvexQuadrilateral([(0, 0), (width, 0), (width, height), (0, height)])

        return PerspectiveUtil.projectQuadrilateralToRectanglePicture(picture, stripe, projectedStripe, width, height)


    def _getLeftStripe(self, quadrilateral):
        bottom = quadrilateral.bottomLeftCorner.y
        left = quadrilateral.bottomLeftCorner.x
        top = quadrilateral.topLeftCorner.y

        width = quadrilateral.bottomRightCorner.x - left
        # FIXME: MAGIC NUMBERS
        right = left + int(width * 0.2)

        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])


    def _getRightStripe(self, quadrilateral):
        bottom = quadrilateral.bottomRightCorner.y
        right = quadrilateral.bottomRightCorner.x
        top = quadrilateral.topRightCorner.y

        width = right - quadrilateral.bottomLeftCorner.x
        # FIXME: MAGIC NUMBERS
        left = right - int(width * 0.2)

        return ConvexQuadrilateral([(left,bottom), (right, bottom), (right, top), (left, top)])


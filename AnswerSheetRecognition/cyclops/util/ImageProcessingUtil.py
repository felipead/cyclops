import cv2

from PerspectiveUtil import *

class ImageProcessingUtil:

    @staticmethod
    def __mapToOddNumber(integer):
        return 2 * integer + 1

    @staticmethod
    def applyEllipticalErosion(image, kernelSize):
        kernelSize = ImageProcessingUtil.__mapToOddNumber(kernelSize)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernelSize, kernelSize))
        return cv2.erode(image, kernel)

    @staticmethod
    def applyEllipticalDilatation(image, kernelSize):
        kernelSize = ImageProcessingUtil.__mapToOddNumber(kernelSize)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernelSize, kernelSize))
        return cv2.dilate(image, kernel)

    @staticmethod
    def applyRectangularDilatation(image, kernelSize):
        kernelSize = ImageProcessingUtil.__mapToOddNumber(kernelSize)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
        return cv2.dilate(image, kernel)

    @staticmethod
    def applyRectangularErosion(image, kernelSize):
        kernelSize = ImageProcessingUtil.__mapToOddNumber(kernelSize)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
        return cv2.erode(image, kernel)

    @staticmethod
    def convertToGrayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def convertToBinaryWithOptimalThreshold(image):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    @staticmethod
    def convertToInvertedBinaryWithOptimalThreshold(image):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return binary

    @staticmethod
    def extractRectangleFromImage(image, quadrilateral):
        left = quadrilateral.bottomLeftCorner.x
        right = quadrilateral.bottomRightCorner.x
        bottom = quadrilateral.bottomRightCorner.y
        top = quadrilateral.topRightCorner.y

        width = right - left
        height = top - bottom

        projectedRectangle = ConvexQuadrilateral([(0, 0), (width, 0), (width, height), (0, height)])

        return PerspectiveUtil.projectQuadrilateralToRectanglePicture(image, quadrilateral, projectedRectangle, width, height)
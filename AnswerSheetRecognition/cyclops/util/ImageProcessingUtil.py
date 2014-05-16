import cv2
import numpy as np

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
    def applyMedianBlur(image, apertureSize):
        return cv2.medianBlur(image, apertureSize)

    @staticmethod
    def applyBilateralFilter(image, filterSize, sigmaColor, sigmaSpace):
        return cv2.bilateralFilter(image, filterSize, sigmaColor, sigmaSpace)


    @staticmethod
    def convertToGrayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    @staticmethod
    def convertToBinaryWithGaussianAdaptativeThreshold(image, blockSize, constantSubtractedFromWeightedMean):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, \
            ImageProcessingUtil.__mapToOddNumber(blockSize), constantSubtractedFromWeightedMean)

    @staticmethod
    def convertToInvertedBinaryWithGaussianAdaptativeThreshold(image, blockSize, constantSubtractedFromWeightedMean):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, \
            ImageProcessingUtil.__mapToOddNumber(blockSize), constantSubtractedFromWeightedMean)

    @staticmethod
    def convertToBinaryWithMeanAdaptativeThreshold(image, blockSize, constantSubtractedFromMean):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, \
            ImageProcessingUtil.__mapToOddNumber(blockSize), constantSubtractedFromMean)

    @staticmethod
    def convertToInvertedBinaryWithMeanAdaptativeThreshold(image, blockSize, constantSubtractedFromMean):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, \
            ImageProcessingUtil.__mapToOddNumber(blockSize), constantSubtractedFromMean)

    
    @staticmethod
    def convertToBinary(image, threshold):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return binary

    @staticmethod
    def convertToInvertedBinary(image, threshold):
        gray = ImageProcessingUtil.convertToGrayscale(image)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        return binary


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
    def extractRectangleFromImage(image, rectangle):
        left = int(rectangle.bottomLeftCorner.x)
        right = int(rectangle.bottomRightCorner.x)
        bottom = int(rectangle.bottomRightCorner.y)
        top = int(rectangle.topRightCorner.y)

        width = right - left
        height = top - bottom

        projectedRectangle = ConvexQuadrilateral([(0, 0), (width, 0), (width, height), (0, height)])

        return PerspectiveUtil.projectQuadrilateralToRectanglePicture(image, rectangle, projectedRectangle, width, height)

    @staticmethod
    def createBlankImage(width, height, colorDepth=np.uint8):
        return np.zeros((height,width,3), colorDepth)

    @staticmethod
    def resizeImage(image, width, height):
        return cv2.resize(image, (width,height))

    @staticmethod
    def getImageSize(image):
        (height, width) = image.shape[:2]
        return (width, height)

    @staticmethod
    def sharpenImageUsingGaussianBlurWeightedDifference(image, originalImageWeight=1.5, bluredImageWeight=0.5, gaussianBlurKernelStandardDeviation=3, gaussianBlurKernelSize=0):
        bluredImage = cv2.GaussianBlur(image, (gaussianBlurKernelSize, gaussianBlurKernelSize), gaussianBlurKernelStandardDeviation)
        return cv2.addWeighted(image, originalImageWeight, bluredImage, -bluredImageWeight, 0)


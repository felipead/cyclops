import cv2
import numpy as np

from .PerspectiveUtil import *


class ImageProcessingUtil:

    @staticmethod
    def __to_odd_number(integer):
        return 2 * integer + 1

    @staticmethod
    def apply_elliptical_erosion(image, kernel_size):
        kernel_size = ImageProcessingUtil.__to_odd_number(kernel_size)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        return cv2.erode(image, kernel)

    @staticmethod
    def apply_elliptical_dilatation(image, kernel_size):
        kernel_size = ImageProcessingUtil.__to_odd_number(kernel_size)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        return cv2.dilate(image, kernel)

    @staticmethod
    def apply_rectangular_dilatation(image, kernel_size):
        kernel_size = ImageProcessingUtil.__to_odd_number(kernel_size)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.dilate(image, kernel)

    @staticmethod
    def apply_rectangular_erosion(image, kernel_size):
        kernel_size = ImageProcessingUtil.__to_odd_number(kernel_size)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.erode(image, kernel)

    @staticmethod
    def apply_median_blur(image, apertureSize):
        return cv2.medianBlur(image, apertureSize)

    @staticmethod
    def apply_bilateral_filter(image, filter_size, sigma_color, sigma_space):
        return cv2.bilateralFilter(image, filter_size, sigma_color, sigma_space)

    @staticmethod
    def convert_to_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def convert_to_binary_with_gaussian_adaptative_threshold(image, block_size, constant_subtracted_from_weighted_mean):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                     ImageProcessingUtil.__to_odd_number(block_size), constant_subtracted_from_weighted_mean)

    @staticmethod
    def convert_to_inverted_binary_with_gaussian_adaptative_threshold(image, block_size, constant_subtracted_from_weighted_mean):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                     ImageProcessingUtil.__to_odd_number(block_size), constant_subtracted_from_weighted_mean)

    @staticmethod
    def convert_to_binaryWithMeanAdaptativeThreshold(image, block_size, constant_subtracted_from_mean):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                     ImageProcessingUtil.__to_odd_number(block_size), constant_subtracted_from_mean)

    @staticmethod
    def convert_to_inverted_binaryWithMeanAdaptativeThreshold(image, block_size, constant_subtracted_from_mean):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                                     ImageProcessingUtil.__to_odd_number(block_size), constant_subtracted_from_mean)

    @staticmethod
    def convert_to_binary(image, threshold):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return binary

    @staticmethod
    def convert_to_inverted_binary(image, threshold):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        return binary

    @staticmethod
    def convert_to_binary_with_optimal_threshold(image):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    @staticmethod
    def convert_to_inverted_binary_with_optimal_threshold(image):
        gray = ImageProcessingUtil.convert_to_grayscale(image)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return binary

    @staticmethod
    def extract_rectangle_from_image(image, rectangle):
        left = int(rectangle.bottom_left_corner.x)
        right = int(rectangle.bottom_right_corner.x)
        bottom = int(rectangle.bottom_right_corner.y)
        top = int(rectangle.top_right_corner.y)

        width = right - left
        height = top - bottom

        projected_rectangle = ConvexQuadrilateral([(0, 0), (width, 0), (width, height), (0, height)])

        return PerspectiveUtil.project_quadrilateral_to_rectangle_picture(image, rectangle, projected_rectangle, width, height)

    @staticmethod
    def create_blank_image(width, height, color_depth=np.uint8):
        return np.zeros((height, width, 3), color_depth)

    @staticmethod
    def resize_image(image, width, height):
        return cv2.resize(image, (width, height))

    @staticmethod
    def get_image_size(image):
        (height, width) = image.shape[:2]
        return (width, height)

    @staticmethod
    def sharpen_image_using_gaussian_blur_weighted_difference(image, original_image_weight=1.5, blured_image_weight=0.5, gaussian_blur_kernel_standard_deviation=3, gaussian_blur_kernel_size=0):
        blured_image = cv2.GaussianBlur(image, (gaussian_blur_kernel_size, gaussian_blur_kernel_size), gaussian_blur_kernel_standard_deviation)
        return cv2.addWeighted(image, original_image_weight, blured_image, -blured_image_weight, 0)

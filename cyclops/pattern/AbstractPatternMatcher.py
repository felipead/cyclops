from abc import *
import cv2
import numpy as np

from .PatternFactory import *
from .PatternMatch import *
from ..util.ImageProcessingUtil import *


class AbstractPatternMatcher:

    __metaclass__ = ABCMeta

    def __init__(self, pattern_name, pattern_sizes):
        self._patterns = []
        for size in pattern_sizes:
            pattern = PatternFactory.get_pattern(pattern_name, size)
            pattern = ImageProcessingUtil.convert_to_grayscale(pattern)
            self._patterns.append(pattern)

    def match(self, picture, number_of_times_to_match):
        matches = []
        for pattern in self._patterns:
            matches.extend(self._match(picture, pattern, number_of_times_to_match))
        return matches

    def _match(self, picture, pattern, number_of_times_to_match):
        picture = ImageProcessingUtil.convert_to_grayscale(picture)
        result = cv2.matchTemplate(picture, pattern, cv2.TM_CCOEFF_NORMED)
        result = cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
        _, result = cv2.threshold(result, 0.5, 1, cv2.THRESH_TOZERO)

        pattern_size = pattern.shape[:2]

        matches = []
        for i in range(number_of_times_to_match):
            _, _, _, max_location = cv2.minMaxLoc(result)
            matches.append(PatternMatch(max_location, pattern_size))

            h, w = result.shape[:2]
            mask = np.zeros((h + 2, w + 2), np.uint8)
            cv2.floodFill(result, mask, max_location, (0, 0, 0), loDiff=(.1, .1, .1), upDiff=(1., 1., 1.))

        return matches

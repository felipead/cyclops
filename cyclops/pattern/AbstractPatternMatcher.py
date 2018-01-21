from abc import *
import cv2
import numpy as np

from .PatternFactory import *
from .PatternMatch import *
from ..util.ImageProcessingUtil import *

class AbstractPatternMatcher:

    __metaclass__ = ABCMeta

    def __init__(self, patternName, patternSizes):
        self._patterns = []
        for patternSize in patternSizes:
            pattern = PatternFactory.getPattern(patternName, patternSize)
            pattern = ImageProcessingUtil.convertToGrayscale(pattern)
            self._patterns.append(pattern)

    def match(self, picture, numberOfTimesToMatch):
        matches = []
        for pattern in self._patterns:
            matches.extend(self._match(picture, pattern, numberOfTimesToMatch))
        return matches

    def _match(self, picture, pattern, numberOfTimesToMatch):
        picture = ImageProcessingUtil.convertToGrayscale(picture)
        result = cv2.matchTemplate(picture, pattern, cv2.TM_CCOEFF_NORMED)
        result = cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
        _, result = cv2.threshold(result, 0.5, 1, cv2.THRESH_TOZERO)

        patternSize = pattern.shape[:2]

        matches = []
        for i in range(numberOfTimesToMatch):
            _, _, _, maxLocation = cv2.minMaxLoc(result)
            matches.append(PatternMatch(maxLocation, patternSize))

            h, w = result.shape[:2]
            mask = np.zeros((h+2, w+2), np.uint8)
            cv2.floodFill(result, mask, maxLocation, (0, 0, 0), loDiff=(.1,.1,.1), upDiff=(1.,1.,1.))

        return matches

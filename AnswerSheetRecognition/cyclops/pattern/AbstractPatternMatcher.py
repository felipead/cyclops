from abc import *

from cv2 import floodFill, cvtColor, matchTemplate, normalize, threshold, minMaxLoc, NORM_MINMAX
from cv import CV_BGR2GRAY, CV_TM_CCOEFF_NORMED, CV_THRESH_TOZERO

import numpy as np

from PatternFactory import *
from PatternMatch import *

class AbstractPatternMatcher:

    __metaclass__ = ABCMeta

    def __init__(self, patternName, patternSizes):
        self._patterns = []
        for patternSize in patternSizes:
            pattern = PatternFactory.getPattern(patternName, patternSize)
            pattern = cvtColor(pattern, CV_BGR2GRAY)
            self._patterns.append(pattern)

    def match(self, picture, numberOfTimesToMatch):
        matches = []
        for pattern in self._patterns:
            matches.extend(self._match(picture, pattern, numberOfTimesToMatch))
        return matches

    def _match(self, picture, pattern, numberOfTimesToMatch):
        picture = cvtColor(picture, CV_BGR2GRAY)
        result = matchTemplate(picture, pattern, CV_TM_CCOEFF_NORMED)
        result = normalize(result, result, 0, 1, NORM_MINMAX, -1)
        _, result = threshold(result, 0.5, 1, CV_THRESH_TOZERO)

        patternSize = pattern.shape[:2]
        
        matches = []
        for i in xrange(numberOfTimesToMatch):
            _, _, _, maxLocation = minMaxLoc(result)
            matches.append(PatternMatch(maxLocation, patternSize))

            h, w = result.shape[:2]
            mask = np.zeros((h+2, w+2), np.uint8)
            floodFill(result, mask, maxLocation, (0, 0, 0), loDiff=(.1,.1,.1), upDiff=(1.,1.,1.))
            # C++ equivalent: cv::floodFill(result, maxLocation, Scalar(0), 0, Scalar(.1), Scalar(1.));

        return matches
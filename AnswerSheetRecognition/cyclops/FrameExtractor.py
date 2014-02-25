from cv2 import *
from cv import *

import numpy as np

from FrameAlignmentPatternMatcher import *
from FrameOrientationPatternMatcher import *

class FrameExtractor:

    def __init__(self):
        self._frameAlignmentPatternMatcher = FrameAlignmentPatternMatcher()
        self._frameOrientationPatternMatcher = FrameOrientationPatternMatcher()

    def extract(self, picture):
        matches =  self._frameAlignmentPatternMatcher.match(picture, 3)
        self._drawTemplateMatch(picture, matches, RGB(255,0,0))

        matches =  self._frameOrientationPatternMatcher.match(picture, 1)
        self._drawTemplateMatch(picture, matches, RGB(0,255,0))

        return matches

    def _drawTemplateMatch(self, picture, matches, highlightColor):
        for match in matches:
            location = match.location
            size = match.size
            rectangle(picture, location, (location[0] + size[0], location[1] + size[1]), highlightColor, 2)
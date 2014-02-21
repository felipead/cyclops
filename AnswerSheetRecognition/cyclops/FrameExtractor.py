from cv2 import *
from cv import *

import numpy as np

class FrameExtractor:

    def __init__(self, circleTemplates, ballTemplates):
        self.circleTemplates = circleTemplates
        self.ballTemplates = ballTemplates

    def extractFrame(self, picture):
        pass

    def matchAllTemplatesAgainst(self, picture):
        for circleTemplate in self.circleTemplates:
            matches = self._matchTemplate(picture, circleTemplate, 3)
            self._drawTemplateMatch(picture, circleTemplate, matches, RGB(255,0,0))

        for ballTemplate in self.ballTemplates:
            matches = self._matchTemplate(picture, ballTemplate, 1)
            self._drawTemplateMatch(picture, ballTemplate, matches, RGB(0,0,255))

    def _matchTemplate(self, picture, template, numberOfTimesToMatch):
        grayPicture = cvtColor(picture, CV_BGR2GRAY)
        grayTemplate = cvtColor(template, CV_BGR2GRAY)
        matchResult = matchTemplate(grayPicture, grayTemplate, CV_TM_CCOEFF_NORMED)
        matchResult = normalize(matchResult, matchResult, 0, 1, NORM_MINMAX, -1)
        _, matchResult = threshold(matchResult, 0.5, 1, CV_THRESH_TOZERO)
        
        matches = []
        for i in xrange(numberOfTimesToMatch):
            minValue, maxValue, minLocation, maxLocation = minMaxLoc(matchResult)
            matches.append((template, maxLocation))

            h, w = matchResult.shape[:2]
            mask = np.zeros((h+2, w+2), np.uint8)
            floodFill(matchResult, mask, maxLocation, (0, 0, 0), loDiff=(.1,.1,.1), upDiff=(1.,1.,1.))
            # C++ equivalent: cv::floodFill(matchResult, maxLocation, Scalar(0), 0, Scalar(.1), Scalar(1.));

        return matches

    def _drawTemplateMatch(self, picture, template, matches, highlightColor):
        templateHeight, templateWidth, _ = template.shape

        for match in matches:
            template = match[0]
            location = match[1]
            rectangle(picture, location, (location[0] + templateWidth, location[1] + templateHeight), highlightColor, 2)
from FrameExtractor import *
from ..util.DrawingUtil import *

class AnswerSheetRecognizer:
    
    def __init__(self):
        self._frameExtractor = FrameExtractor()

    def recognize(self, mainPicture):
        result = self._frameExtractor.extractFrames(mainPicture)

        for match in result.frameOrientationMatches:
            DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_BLUE, 1)
        for match in result.frameAlignmentMatches:
            DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_GREEN, 1)

        if result.answerSheetMatchFrame != None:
            DrawingUtil.drawQuadrilateralLines(mainPicture, result.answerSheetMatchFrame.originalQuadrilateral, DrawingUtil.COLOR_RED, 1)
            if result.answerSheetMismatchQuadrilaterals != None:
                for mismatchQuadrilateral in result.answerSheetMismatchQuadrilaterals:
                    DrawingUtil.drawQuadrilateralLines(mainPicture, mismatchQuadrilateral, DrawingUtil.COLOR_WHITE, 1)
            return result.answerSheetMatchFrame.projectedPicture

        return None
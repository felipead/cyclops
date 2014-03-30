from AnswerSheetFrameExtractor import *
from ..util.DrawingUtil import *

class AnswerSheetRecognizer:
    
    def __init__(self):
        self._answerSheetFrameExtractor = AnswerSheetFrameExtractor()

    def recognize(self, mainPicture):
        answerSheetFrameResult = self._answerSheetFrameExtractor.extract(mainPicture)

        for match in answerSheetFrameResult.frameOrientationMatches:
            DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_BLUE, 1)
        for match in answerSheetFrameResult.frameAlignmentMatches:
            DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_GREEN, 1)

        if answerSheetFrameResult.answerSheetMatchFrame != None:
            DrawingUtil.drawQuadrilateralLines(mainPicture, answerSheetFrameResult.answerSheetMatchFrame.originalQuadrilateral, DrawingUtil.COLOR_RED, 1)
            if answerSheetFrameResult.answerSheetMismatchQuadrilaterals != None:
                for mismatchQuadrilateral in answerSheetFrameResult.answerSheetMismatchQuadrilaterals:
                    DrawingUtil.drawQuadrilateralLines(mainPicture, mismatchQuadrilateral, DrawingUtil.COLOR_WHITE, 1)
            return answerSheetFrameResult.answerSheetMatchFrame.projectedPicture

        return None
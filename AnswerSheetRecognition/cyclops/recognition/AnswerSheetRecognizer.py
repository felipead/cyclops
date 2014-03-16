from FrameExtractor import *
from ..util.DrawingUtil import *

class AnswerSheetRecognizer:
    
    def __init__(self):
        self._frameExtractor = FrameExtractor()

    def recognize(self, mainPicture):
        result = self._frameExtractor.extractFrames(mainPicture)

#        for match in result.frameOrientationMatches:
#            DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_BLUE)
#        for match in result.frameAlignmentMatches:
#            DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_GREEN)

        if result.answerSheetFrame != None:
            self._drawFrame(mainPicture, result.answerSheetFrame)
            return result.answerSheetFrame.alignedPicture

        return None

    def _drawFrame(self, picture, frame):
        originalQuadrilateral = frame.originalQuadrilateral
        alignedQuadrilateral = frame.alignedQuadrilateral

        DrawingUtil.drawQuadrilateralLines(picture, originalQuadrilateral.vertexes, DrawingUtil.COLOR_RED, 1)
        DrawingUtil.drawQuadrilateralLines(picture, alignedQuadrilateral.vertexes, DrawingUtil.COLOR_WHITE, 1)

        DrawingUtil.drawFilledCircle(picture, alignedQuadrilateral[0], 5, DrawingUtil.COLOR_YELLOW)
        for vertex in originalQuadrilateral.vertexes:
            DrawingUtil.drawFilledCircle(picture, vertex, 1, DrawingUtil.COLOR_YELLOW)
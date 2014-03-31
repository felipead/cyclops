from AnswerSheetFrameExtractor import *
from QrCodeFrameExtractor import *
from AnswerSheetRecognitionResult import *
from Frame import *

from ..util.DrawingUtil import *

class AnswerSheetRecognizer:
    
    def __init__(self):
        self._answerSheetFrameExtractor = AnswerSheetFrameExtractor()
        self._qrCodeFrameExtractor = QrCodeFrameExtractor()

    def recognize(self, mainPicture):
        answerSheetFrameExtractionResult = self._answerSheetFrameExtractor.extract(mainPicture)

        qrCodeFrame = None
        answerSheetFrame = None
        if answerSheetFrameExtractionResult.answerSheetMatchFrame != None:
            answerSheetFrame = answerSheetFrameExtractionResult.answerSheetMatchFrame
            qrCodeFrame = self._qrCodeFrameExtractor.extract(mainPicture, answerSheetFrame)

        # FIXME: DEBUG INFO
        # for match in answerSheetFrameExtractionResult.frameOrientationMatches:
        #     DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_BLUE, 1)
        # for match in answerSheetFrameExtractionResult.frameAlignmentMatches:
        #     DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_GREEN, 1)

        if answerSheetFrame != None:
            DrawingUtil.drawQuadrilateralLines(mainPicture, answerSheetFrame.originalQuadrilateral, DrawingUtil.COLOR_RED, 1)
            if answerSheetFrameExtractionResult.answerSheetMismatchQuadrilaterals != None:
                for mismatchQuadrilateral in answerSheetFrameExtractionResult.answerSheetMismatchQuadrilaterals:
                    DrawingUtil.drawQuadrilateralLines(mainPicture, mismatchQuadrilateral, DrawingUtil.COLOR_WHITE, 1)

        if qrCodeFrame != None:
            DrawingUtil.drawQuadrilateralLines(mainPicture, qrCodeFrame.originalQuadrilateral, DrawingUtil.COLOR_RED, 1)

        result = AnswerSheetRecognitionResult()
        result.answerSheetFrame = answerSheetFrame
        result.qrCodeFrame = qrCodeFrame
        return result
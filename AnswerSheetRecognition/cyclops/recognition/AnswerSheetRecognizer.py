from AnswerFrameExtractor import *
from QrCodeFrameExtractor import *
from AnswerSheetRecognitionResult import *
from QrCodeDecoder import *
from AnswerFrameRecognizer import *

class AnswerSheetRecognizer:
    
    def __init__(self):
        self._answerFrameExtractor = AnswerFrameExtractor()
        self._qrCodeFrameExtractor = QrCodeFrameExtractor()
        self._qrCodeDecoder = QrCodeDecoder()
        self._answerFrameRecognizer = AnswerFrameRecognizer()

    def recognize(self, picture):
        result = AnswerSheetRecognitionResult()

        extraction = self._answerFrameExtractor.extract(picture)
        if extraction.answerFrame != None:
            qrCodeFrame = self._qrCodeFrameExtractor.extract(extraction.answerFrame)
            qrCodeData = self._qrCodeDecoder.decode(qrCodeFrame)
            
            result.answerFrame = extraction.answerFrame
            result.qrCodeFrame = qrCodeFrame
            result.qrCodeData = qrCodeData

        # FIXME: TEMPORARY DEBUG INFO
        # for match in answerFrameExtraction.frameOrientationPatternMatches:
        #     DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_BLUE, 1)
        # for match in answerFrameExtraction.frameAlignmentPatternMatches:
        #     DrawingUtil.drawRectangle(mainPicture, match.location, match.size, DrawingUtil.COLOR_GREEN, 1)
        # if extraction.answerFrameMismatches != None:
        #     for answerFrameMismatch in extraction.answerFrameMismatches:
        #         DrawingUtil.drawQuadrilateralLines(picture, answerFrameMismatch, DrawingUtil.COLOR_WHITE, 1)

        return result
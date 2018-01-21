from .AnswerFrameExtractor import *
from .QrCodeFrameExtractor import *
from .AnswerSheetRecognitionResult import *
from .QrCodeDecoder import *
from .AnswerFrameRecognizer import *


class AnswerSheetRecognizer:

    def __init__(self):
        self._answer_frame_extractor = AnswerFrameExtractor()
        self._qr_code_frame_extractor = QrCodeFrameExtractor()
        self._qr_code_decoder = QrCodeDecoder()
        self._answer_frameRecognizer = AnswerFrameRecognizer()

    def recognize(self, picture):
        result = AnswerSheetRecognitionResult()

        extraction = self._answer_frame_extractor.extract(picture)
        if extraction.answer_frame is not None:
            qr_code_frame = self._qr_code_frame_extractor.extract(extraction.answer_frame)
            qr_code_data = self._qr_code_decoder.decode(qr_code_frame)

            if qr_code_data is not None:
                self._answer_frameRecognizer.recognize(extraction.answer_frame, qr_code_data)

            result.answer_frame = extraction.answer_frame
            result.qr_code_frame = qr_code_frame
            result.qr_code_data = qr_code_data

        # FIXME: DEBUG INFO
        for match in extraction.frame_orientation_matches:
            DrawingUtil.draw_rectangle(picture, match.location, match.size, DrawingUtil.COLOR_BLUE, 1)
        for match in extraction.frame_alignment_matches:
            DrawingUtil.draw_rectangle(picture, match.location, match.size, DrawingUtil.COLOR_GREEN, 1)
        if extraction.answer_frame_mismatches is not None:
            for answer_frameMismatch in extraction.answer_frame_mismatches:
                DrawingUtil.draw_quadrilateral_lines(picture, answer_frameMismatch, DrawingUtil.COLOR_WHITE, 1)

        return result

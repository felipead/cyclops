from FrameExtractor import *

class AnswerSheetRecognizer:
    
    def __init__(self):
        self._frameExtractor = FrameExtractor()

    def recognize(self, picture):
        self._frameExtractor.extract(picture)
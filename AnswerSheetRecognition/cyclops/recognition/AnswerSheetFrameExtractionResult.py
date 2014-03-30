class AnswerSheetFrameExtractionResult:

    def __init__(self):
        self.answerSheetMatchFrame = None
        self.answerSheetMismatchQuadrilaterals = []
        self.qrCodeFrame = None
        self.frameOrientationMatches = []
        self.frameAlignmentMatches = []
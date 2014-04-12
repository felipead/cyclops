class QrCodeData:

    def __init__(self):
        self.rawString = None
        self.answerSheetId = None
        self.numberOfQuestions = None
        self.numberOfAnswerChoices = None

    def __str__(self):
        return self.rawString
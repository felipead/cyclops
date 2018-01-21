class QrCodeData:

    def __init__(self):
        self.raw_string = None
        self.answer_sheet_id = None
        self.number_questions = None
        self.number_answer_choices = None
        self.number_questions_per_column = None

    def __str__(self):
        return self.raw_string

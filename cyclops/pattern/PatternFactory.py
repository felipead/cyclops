import os

from cv2 import imread

class PatternFactory:

    PATTERN_FOLDER = 'Patterns'
    PATTERN_FILE_EXTENSION = '.png'
    PATTERN_FILE_NAME_SEPARATOR = '_'

    @classmethod
    def _getPatternFileName(self, name, size):
        return name + PatternFactory.PATTERN_FILE_NAME_SEPARATOR + str(size) + PatternFactory.PATTERN_FILE_EXTENSION

    @classmethod
    def getPattern(self, name, size):
        path = os.path.join(PatternFactory.PATTERN_FOLDER, self._getPatternFileName(name, size))
        return imread(path)


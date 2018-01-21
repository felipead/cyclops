import os
import cv2


class PatternFactory:

    PATTERN_FOLDER = 'Patterns'
    PATTERN_FILE_EXTENSION = '.png'
    PATTERN_FILE_NAME_SEPARATOR = '_'

    @classmethod
    def _get_pattern_filename(self, name, size):
        return name + PatternFactory.PATTERN_FILE_NAME_SEPARATOR + str(size) + PatternFactory.PATTERN_FILE_EXTENSION

    @classmethod
    def get_pattern(self, name, size):
        path = os.path.join(PatternFactory.PATTERN_FOLDER, self._get_pattern_filename(name, size))
        return cv2.imread(path)

import unittest
from unittest import TestCase

from ..PatternFactory import *

class PatternFactoryTest(TestCase):

    def setUp(self):
        pass

    def testGetFrameAlignmentPattern(self):
        assert PatternFactory.getPattern("FrameAlignment", 32).shape[:2] == (32,32)
        assert PatternFactory.getPattern("FrameAlignment", 48).shape[:2] == (48,48)

    def testGetFrameOrientationPattern(self):
        assert PatternFactory.getPattern("FrameOrientation", 32).shape[:2] == (32,32)
        assert PatternFactory.getPattern("FrameOrientation", 48).shape[:2] == (48,48)

if __name__ == "__main__":
    unittest.main()
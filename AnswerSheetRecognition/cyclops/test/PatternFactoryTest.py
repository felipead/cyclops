import unittest
from unittest import TestCase

from ..PatternFactory import *

class PatternFactoryTest(TestCase):

    def setUp(self):
        pass

    def testGetFrameAlignmentPattern(self):
        assert PatternFactory.getPattern("FrameAlignment", 30).shape[:2] == (30,30)
        assert PatternFactory.getPattern("FrameAlignment", 45).shape[:2] == (45,45)

    def testGetFrameOrientationPattern(self):
        assert PatternFactory.getPattern("FrameOrientation", 30).shape[:2] == (30,30)
        assert PatternFactory.getPattern("FrameOrientation", 45).shape[:2] == (45,45)

if __name__ == "__main__":
    unittest.main()
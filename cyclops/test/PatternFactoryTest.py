import unittest
from unittest import TestCase

from ..pattern.PatternFactory import *

class PatternFactoryTest(TestCase):

    def test_get_frame_alignment_pattern(self):
        assert PatternFactory.get_pattern('FrameAlignment', 32).shape[:2] == (32,32)
        assert PatternFactory.get_pattern('FrameAlignment', 48).shape[:2] == (48,48)

    def test_get_frame_orientation_pattern(self):
        assert PatternFactory.get_pattern('FrameOrientation', 32).shape[:2] == (32,32)
        assert PatternFactory.get_pattern('FrameOrientation', 48).shape[:2] == (48,48)

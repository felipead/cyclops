from ..pattern.PatternFactory import *


def test_get_frame_alignment_pattern():
    assert PatternFactory.get_pattern('FrameAlignment', 32).shape[:2] == (32, 32)
    assert PatternFactory.get_pattern('FrameAlignment', 48).shape[:2] == (48, 48)


def test_get_frame_orientation_pattern():
    assert PatternFactory.get_pattern('FrameOrientation', 32).shape[:2] == (32, 32)
    assert PatternFactory.get_pattern('FrameOrientation', 48).shape[:2] == (48, 48)

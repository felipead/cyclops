import pytest

from ..recognition.AnswerFrameExtractor import *
from ..util.MathUtil import *
from ..geometry.ConvexQuadrilateral import *
from ..pattern.PatternMatch import *


@pytest.fixture
def size_relaxation_ratio():
    return 1.10

@pytest.fixture
def angle_relaxation_radians():
    return 0.2

@pytest.fixture
def extractor(size_relaxation_ratio, angle_relaxation_radians):
    return AnswerFrameExtractor(size_relaxation_ratio, angle_relaxation_radians)

def find_answer_frames_quadrilaterals_runner(extractor, frame_orientation_matches, frame_alignment_matches, expected_frames):
    found_frames = extractor._find_answer_frame_quadrilaterals(frame_orientation_matches, frame_alignment_matches)
    for frame in expected_frames:
        assert frame in found_frames

def build_pattern_matches(centers, size):
    matches = []
    for center in centers:
        matches.append(PatternMatch.from_center(center, size))
    return matches


def test_find_convex_quadrilaterals_with_roughly_equal_sizes_and_angles(extractor, angle_relaxation_radians):
    base_point=(125, 98)
    other_points=[(135, 327), (359, 333), (364, 99), (552, 210), (285, 169), (362, 99)]
    quadrilaterals = extractor._find_convex_quadrilaterals_with_roughly_equal_sizes_and_angles(base_point, other_points)
    assert ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (364, 99)]) in quadrilaterals
    assert ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (362, 99)]) in quadrilaterals
    for quadrilateral in quadrilaterals:
        assert quadrilateral.has_right_interior_angles_with_relaxation_of(angle_relaxation_radians)


def test_find_answer_frame_quadrilaterals_sample01(extractor):
    match_size = (32,32)
    frame_orientation_matches = build_pattern_matches([(37, 266), (492, 343)], match_size)
    frame_alignment_matches = build_pattern_matches([(142, 16), (622, 371), (190, 259), (526, 72), (248, 45), (228, 314)], match_size)
    expected_frames = []
    expected_frames.append(ConvexQuadrilateral([(492, 343), (526, 72), (248, 45), (228, 314)]))
    find_answer_frames_quadrilaterals_runner(extractor, frame_orientation_matches, frame_alignment_matches, expected_frames)

def test_find_answer_frame_quadrilaterals_sample02(extractor):
    match_size = (32,32)
    frame_orientation_matches = build_pattern_matches([(624, 161), (519, 368)], match_size)
    frame_alignment_matches = build_pattern_matches([(169, 353), (89, 397), (80, 397), (216, 370), (538, 56), (204, 56)], match_size)
    expected_frames = []
    expected_frames.append(ConvexQuadrilateral([(519, 368), (538, 56), (204, 56), (216, 370)]))
    find_answer_frames_quadrilaterals_runner(extractor, frame_orientation_matches, frame_alignment_matches, expected_frames)

def test_find_answer_frame_quadrilaterals_sample03(extractor):
    match_size = (32,32)
    frame_orientation_matches = build_pattern_matches([(526, 363), (519, 364)], match_size)
    frame_alignment_matches = build_pattern_matches([(171, 344), (89, 303), (81, 309), (535, 54), (213, 51), (218, 362)], match_size)
    expected_frames = []
    expected_frames.append(ConvexQuadrilateral([(526, 363), (535, 54), (213, 51), (218, 362)]))
    expected_frames.append(ConvexQuadrilateral([(519, 364), (535, 54), (213, 51), (218, 362)]))
    find_answer_frames_quadrilaterals_runner(extractor, frame_orientation_matches, frame_alignment_matches, expected_frames)

def test_find_answer_frame_quadrilaterals_sample04(extractor):
    match_size = (32,32)
    frame_orientation_matches = build_pattern_matches([(180, 368), (580, 239)], match_size)
    frame_alignment_matches = build_pattern_matches([(417, 360), (417, 130), (182, 127), (119, 159), (481, 195), (251, 205)], match_size)
    expected_frames = []
    expected_frames.append(ConvexQuadrilateral([(180, 368), (417, 360), (417, 130), (182, 127)]))
    find_answer_frames_quadrilaterals_runner(extractor, frame_orientation_matches, frame_alignment_matches, expected_frames)

def test_find_answer_frame_quadrilaterals_sample05(extractor):
    match_size = (32,32)
    frame_orientation_matches = build_pattern_matches([(125, 98), (121, 96)], match_size)
    frame_alignment_matches = build_pattern_matches([(135, 327), (359, 333), (364, 99), (552, 210), (285, 169), (362, 99)], match_size)
    expected_frames = []
    expected_frames.append(ConvexQuadrilateral([(121, 96), (135, 327), (359, 333), (362, 99)]))
    expected_frames.append(ConvexQuadrilateral([(121, 96), (135, 327), (359, 333), (364, 99)]))
    expected_frames.append(ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (364, 99)]))
    expected_frames.append(ConvexQuadrilateral([(125, 98), (135, 327), (359, 333), (362, 99)]))
    find_answer_frames_quadrilaterals_runner(extractor, frame_orientation_matches, frame_alignment_matches, expected_frames)

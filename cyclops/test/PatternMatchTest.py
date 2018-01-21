from ..pattern.PatternMatch import *


def test_get_center():
    match = PatternMatch(location=(10,50), size=(10,20))
    assert match.center == (15,60)

def test_from_center():
    center = (100, 200)
    size = (50, 100)
    match = PatternMatch.from_center(center, size)
    assert match.center == center
    assert match.size == size
    assert match.location == (75, 150)

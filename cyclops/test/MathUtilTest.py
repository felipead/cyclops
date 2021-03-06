from math import sqrt

from ..util.MathUtil import *


def test_distance_between_points():
    assert MathUtil.distance_between_points((3, 3), (1, 3)) == 2
    assert MathUtil.distance_between_points((3, 1), (3, 3)) == 2

    assert MathUtil.distance_between_points((-4, 1), (3, 1)) == 7
    assert MathUtil.distance_between_points((5, 5), (5, 5)) == 0
    assert MathUtil.distance_between_points((-2, 3), (1, -1)) == 5


def test_equal_within_error():
    assert MathUtil.equal_within_error(5.32, 5.34, 0.1)
    assert MathUtil.equal_within_error(5.32, 5.34, 0.02)
    assert not MathUtil.equal_within_error(5.32, 5.34, 0.01)

    assert MathUtil.equal_within_error(690, 695, 9)
    assert MathUtil.equal_within_error(690, 695, 5)
    assert not MathUtil.equal_within_error(690, 695, 4)


def test_equal_within_fraction():
    assert MathUtil.equal_within_ratio(6, 4, 1.5)
    assert MathUtil.equal_within_ratio(4, 6, 1.5)
    assert MathUtil.equal_within_ratio(5, 4, 1.25)
    assert MathUtil.equal_within_ratio(4, 5, 1.25)

    assert not MathUtil.equal_within_ratio(5, 4, 1.2499999)
    assert not MathUtil.equal_within_ratio(4, 5, 1.2499999)
    assert not MathUtil.equal_within_ratio(4, 5, 1.0)
    assert not MathUtil.equal_within_ratio(4, 5, 0.80)

    assert MathUtil.equal_within_ratio(-30, -40, 1.333334)
    assert MathUtil.equal_within_ratio(6.90, 3.45, 2)


def test_sign():
    assert MathUtil.sign(-1) == -1
    assert MathUtil.sign(-50.15) == -1
    assert MathUtil.sign(+30.99) == +1
    assert MathUtil.sign(+1) == +1
    assert MathUtil.sign(0) == 0

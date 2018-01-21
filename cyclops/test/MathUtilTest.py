import unittest
from unittest import TestCase

from math import sqrt

from ..util.MathUtil import *

class MathUtilTest(TestCase):

    def test_distance_between_points(self):
        assert MathUtil.distance_between_points((3,3), (1,3)) == 2
        assert MathUtil.distance_between_points((3,1), (3,3)) == 2

        assert MathUtil.distance_between_points((-4,1), (3,1)) == 7

        assert MathUtil.distance_between_points((5,5), (5,5)) == 0

        assert MathUtil.distance_between_points((-2,3), (1,-1)) == 5


    def test_equal_within_error(self):
        assert MathUtil.equal_within_error(5.32, 5.34, 0.1) == True
        assert MathUtil.equal_within_error(5.32, 5.34, 0.02) == True
        assert MathUtil.equal_within_error(5.32, 5.34, 0.01) == False

        assert MathUtil.equal_within_error(690, 695, 9) == True
        assert MathUtil.equal_within_error(690, 695, 5) == True
        assert MathUtil.equal_within_error(690, 695, 4) == False

    def test_equal_within_fraction(self):
        assert MathUtil.equal_within_ratio(6, 4, 1.5) == True
        assert MathUtil.equal_within_ratio(4, 6, 1.5) == True
        assert MathUtil.equal_within_ratio(5, 4, 1.25) == True
        assert MathUtil.equal_within_ratio(4, 5, 1.25) == True

        assert MathUtil.equal_within_ratio(5, 4, 1.2499999) == False
        assert MathUtil.equal_within_ratio(4, 5, 1.2499999) == False
        assert MathUtil.equal_within_ratio(4, 5, 1.0) == False
        assert MathUtil.equal_within_ratio(4, 5, 0.80) == False

        assert MathUtil.equal_within_ratio(-30, -40, 1.333334) == True
        assert MathUtil.equal_within_ratio(6.90, 3.45, 2) == True

    def test_sign(self):
        assert MathUtil.sign(-1) == -1
        assert MathUtil.sign(-50.15) == -1
        assert MathUtil.sign(+30.99) == +1
        assert MathUtil.sign(+1) == +1
        assert MathUtil.sign(0) == 0

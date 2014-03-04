import unittest
from unittest import TestCase

from math import sqrt

from ..util.MathUtil import *

class MathUtilTest(TestCase):

    def testDistanceBetweenPoints(self):
        assert MathUtil.distanceBetweenPoints((3,3), (1,3)) == 2
        assert MathUtil.distanceBetweenPoints((3,1), (3,3)) == 2

        assert MathUtil.distanceBetweenPoints((-4,1), (3,1)) == 7
        
        assert MathUtil.distanceBetweenPoints((5,5), (5,5)) == 0

        assert MathUtil.distanceBetweenPoints((-2,3), (1,-1)) == 5


    def testEqualWithinError(self):
        assert MathUtil.equalWithinError(5.32, 5.34, 0.1) == True
        assert MathUtil.equalWithinError(5.32, 5.34, 0.02) == True
        assert MathUtil.equalWithinError(5.32, 5.34, 0.01) == False

        assert MathUtil.equalWithinError(690, 695, 9) == True
        assert MathUtil.equalWithinError(690, 695, 5) == True
        assert MathUtil.equalWithinError(690, 695, 4) == False

    def testEqualWithinFraction(self):
        assert MathUtil.equalWithinRatio(6, 4, 1.5) == True
        assert MathUtil.equalWithinRatio(4, 6, 1.5) == True
        assert MathUtil.equalWithinRatio(5, 4, 1.25) == True
        assert MathUtil.equalWithinRatio(4, 5, 1.25) == True

        assert MathUtil.equalWithinRatio(5, 4, 1.2499999) == False
        assert MathUtil.equalWithinRatio(4, 5, 1.2499999) == False
        assert MathUtil.equalWithinRatio(4, 5, 1.0) == False
        assert MathUtil.equalWithinRatio(4, 5, 0.80) == False

        assert MathUtil.equalWithinRatio(-30, -40, 1.333334) == True
        assert MathUtil.equalWithinRatio(6.90, 3.45, 2) == True
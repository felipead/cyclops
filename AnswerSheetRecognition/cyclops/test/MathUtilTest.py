import unittest
from unittest import TestCase

from math import sqrt

from ..MathUtil import *

class MathUtilTest(TestCase):

    def testDistanceBetween2dPoints(self):
        assert MathUtil.distanceBetweenPoints((3,3), (1,3)) == 2
        assert MathUtil.distanceBetweenPoints((3,1), (3,3)) == 2

        assert MathUtil.distanceBetweenPoints((-4,1), (3,1)) == 7
        
        assert MathUtil.distanceBetweenPoints((5,5), (5,5)) == 0

        assert MathUtil.distanceBetweenPoints((-2,3), (1,-1)) == 5


    def testEqualsWithinError(self):
        assert MathUtil.isEqualsWithinError(5.32, 5.34, 0.1) == True
        assert MathUtil.isEqualsWithinError(5.32, 5.34, 0.02) == True
        assert MathUtil.isEqualsWithinError(5.32, 5.34, 0.01) == False

        assert MathUtil.isEqualsWithinError(690, 695, 9) == True
        assert MathUtil.isEqualsWithinError(690, 695, 5) == True
        assert MathUtil.isEqualsWithinError(690, 695, 4) == False

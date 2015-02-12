import unittest
from unittest import TestCase

from ..pattern.PatternMatch import *

class PatternMatchTest(TestCase):

    def testGetCenter(self):
        match = PatternMatch(location=(10,50), size=(10,20))
        assert match.center == (15,60)

    def testFromCenter(self):
        center = (100, 200)
        size = (50, 100)
        match = PatternMatch.fromCenter(center, size)
        assert match.center == center
        assert match.size == size
        assert match.location == (75, 150)
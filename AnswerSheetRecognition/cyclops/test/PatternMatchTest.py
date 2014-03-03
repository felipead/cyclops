import unittest
from unittest import TestCase

from ..PatternMatch import *

class PatternMatchTest(TestCase):

    def testGetCenter(self):
        match = PatternMatch(location=(10,50), size=(10,20))
        assert match.center == (15,60)
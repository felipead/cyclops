import unittest
from unittest import *

from FrameExtractorTest import *
from PatternFactoryTest import *
from PatternMatchTest import *
from MathUtilTest import *
from VectorTest import *
from QuadrilateralTest import *

ALL_TESTS = (
    makeSuite(FrameExtractorTest),
    makeSuite(PatternFactoryTest),
    makeSuite(MathUtilTest),
    makeSuite(PatternMatchTest),
    makeSuite(VectorTest),
    makeSuite(QuadrilateralTest)
)


def main():
    runner = TextTestRunner()
    runner.run(TestSuite(ALL_TESTS))


if __name__ == "__main__":
    main()

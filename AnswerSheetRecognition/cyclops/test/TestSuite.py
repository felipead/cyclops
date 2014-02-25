import unittest
from unittest import *

from FrameExtractorTest import *
from PatternFactoryTest import *


ALL_TESTS = (
    makeSuite(FrameExtractorTest),
    makeSuite(PatternFactoryTest)
)


def main():
    runner = TextTestRunner()
    runner.run(TestSuite(ALL_TESTS))


if __name__ == "__main__":
    main()

import unittest
from unittest import *

from DigraphTest import *
from DigraphBuilderTest import *
from SolutionTest import *
from TreeTest import *


ALL_TESTS = (
    makeSuite(DigraphTest),
    makeSuite(DigraphBuilderTest),
    makeSuite(TreeTest),
    makeSuite(SolutionTest)
)


def main():
    runner = TextTestRunner()
    runner.run(TestSuite(ALL_TESTS))


if __name__ == "__main__":
    main()

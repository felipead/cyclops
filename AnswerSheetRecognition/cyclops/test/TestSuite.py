import unittest
from unittest import *

from FrameExtractorTest import *
from PatternFactoryTest import *
from PatternMatchTest import *
from MathUtilTest import *
from PointTest import *
from VectorTest import *
from PolygonTest import *
from ConvexPolygonTest import *
from ConvexQuadrilateralTest import *
from SquareTest import *

ALL_TESTS = (
    makeSuite(MathUtilTest),
    makeSuite(PointTest),
    makeSuite(VectorTest),
    makeSuite(PolygonTest),
    makeSuite(ConvexPolygonTest),
    makeSuite(ConvexQuadrilateralTest),
    makeSuite(SquareTest),
    makeSuite(PatternFactoryTest),
    makeSuite(PatternMatchTest),
    makeSuite(FrameExtractorTest)
)


def main():
    runner = TextTestRunner()
    runner.run(TestSuite(ALL_TESTS))


if __name__ == "__main__":
    main()

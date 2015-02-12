import unittest
from unittest import *

from AnswerFrameExtractorTest import *
from PatternFactoryTest import *
from PatternMatchTest import *
from MathUtilTest import *
from OrientationUtilTest import *
from PointTest import *
from VectorTest import *
from PolygonTest import *
from ConvexPolygonTest import *
from ConvexQuadrilateralTest import *
from GeometryUtilTest import *

ALL_TESTS = (
    makeSuite(MathUtilTest),
    makeSuite(OrientationUtilTest),
    makeSuite(PointTest),
    makeSuite(VectorTest),
    makeSuite(PolygonTest),
    makeSuite(ConvexPolygonTest),
    makeSuite(ConvexQuadrilateralTest),
    makeSuite(PatternFactoryTest),
    makeSuite(PatternMatchTest),
    makeSuite(AnswerFrameExtractorTest),
    makeSuite(GeometryUtilTest)
)


def main():
    runner = TextTestRunner()
    runner.run(TestSuite(ALL_TESTS))


if __name__ == "__main__":
    main()

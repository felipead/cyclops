import cv2 as cv
import numpy as np

from ..geometry.ConvexQuadrilateral import *

class PerspectiveUtil:
    
    @staticmethod
    def projectQuadrilateralToSquarePicture(picture, quadrilateralToBeProjected, squareToProject):
        size = int(squareToProject.largestSideLength)
        return PerspectiveUtil.projectQuadrilateralToRectanglePicture(picture, quadrilateralToBeProjected, squareToProject, size, size)

    @staticmethod
    def projectQuadrilateralToRectanglePicture(picture, quadrilateralToBeProjected, rectangleToProject, width, heigth):
        sourcePoints = np.array(PerspectiveUtil.__asListOf2dTuples(quadrilateralToBeProjected), np.float32)
        targetPoints = np.array(PerspectiveUtil.__asListOf2dTuples(rectangleToProject), np.float32)

        transformMatrix = cv.getPerspectiveTransform(sourcePoints, targetPoints)
        return cv.warpPerspective(picture, transformMatrix, (width, heigth))

    @staticmethod
    def __asListOf2dTuples(quadrilateral):
        l = []
        for v in quadrilateral.vertexes:
            l.append(v.as2dTuple())
        return l
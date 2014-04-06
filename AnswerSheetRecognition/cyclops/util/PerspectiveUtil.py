import cv2 as cv
import numpy as np

from ..geometry.ConvexQuadrilateral import *

class PerspectiveUtil:
    
    @staticmethod
    def projectQuadrilateralToSquarePicture(picture, quadrilateralToBeProjected, squareToProject):
        sourcePoints = np.array(PerspectiveUtil.__asListOf2dTuples(quadrilateralToBeProjected), np.float32)
        targetPoints = np.array(PerspectiveUtil.__asListOf2dTuples(squareToProject), np.float32)

        transformMatrix = cv.getPerspectiveTransform(sourcePoints, targetPoints)
        
        size = int(squareToProject.largestSideLength)
        return cv.warpPerspective(picture, transformMatrix, (size,size))

    @staticmethod
    def __asListOf2dTuples(quadrilateral):
        l = []
        for v in quadrilateral.vertexes:
            l.append(v.as2dTuple())
        return l
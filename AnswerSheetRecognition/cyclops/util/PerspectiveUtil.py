from cv2 import getPerspectiveTransform, warpPerspective
import numpy as np

from ..geometry.ConvexQuadrilateral import *

class PerspectiveUtil:
    
    @staticmethod
    def projectQuadrilateralToSquarePicture(picture, quadrilateralToBeProjected, squareToProject):
        sourcePoints = np.array(quadrilateralToBeProjected.asListOfTuples(), np.float32)
        targetPoints = np.array(squareToProject.asListOfTuples(), np.float32)

        transformMatrix = getPerspectiveTransform(sourcePoints, targetPoints)
        
        size = int(squareToProject.largestSideLength)
        return warpPerspective(picture, transformMatrix, (size,size))
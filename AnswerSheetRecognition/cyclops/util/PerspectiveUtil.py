from cv2 import getPerspectiveTransform, warpPerspective
import numpy as np

from ..geometry.ConvexQuadrilateral import *

class PerspectiveUtil:
    
    @staticmethod
    def projectQuadrilateralInsidePictureToSquarePicture(picture, quadrilateral):
        projectedSquare = quadrilateral.projectToSquare()

        size = projectedSquare.largestSideLength
        target = np.zeros((size,size,3), picture.dtype)
        width, height = target.shape[:2]
        target_points = np.array([(0, 0), (height - 1, 0), (height - 1, width - 1), (0, width - 1)], np.float32)

        source_points = np.array(quadrilateral.vertexes, np.float32)
        trans_mat = getPerspectiveTransform(source_points, target_points)
        warped = warpPerspective(picture, trans_mat, (height, width))

        return warped

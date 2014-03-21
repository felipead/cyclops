from cv2 import getPerspectiveTransform, warpPerspective, transpose, flip
import numpy as np

from ..geometry.ConvexQuadrilateral import *
from OrientationUtil import *

class PerspectiveUtil:
    
    # FIXME: WORK IN PROGRESS
    @staticmethod
    def projectQuadrilateralInsidePictureToSquarePicture(picture, quadrilateral):

        #quadrilateral = OrientationUtil.orientQuadrilateral(quadrilateral, quadrilateral[0])

        size = quadrilateral.largestSideLength
        target = np.zeros((size,size,3), picture.dtype)
        width, height = target.shape[:2]
        
        target_points = np.array([(0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)], np.float32)

        vertexes = []
        if quadrilateral.isClockwise:
            vertexes = [quadrilateral[0], quadrilateral[3], quadrilateral[2], quadrilateral[1]]
        else:
            vertexes = [quadrilateral[0], quadrilateral[1], quadrilateral[2], quadrilateral[3]]
        source_points = np.array(vertexes, np.float32)

        trans_mat = getPerspectiveTransform(source_points, target_points)
        warpedPicture = warpPerspective(picture, trans_mat, (width, height))

        return warpedPicture

        # orientedPicture = warpedPicture
        # n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(quadrilateral, quadrilateral[0])
        # for i in xrange(n):
        #     orientedPicture = PerspectiveUtil.rotatePicture90DegreesClockwise(orientedPicture)
        # return orientedPicture


    @staticmethod
    def rotatePicture90DegreesClockwise(picture):
        width, height = picture.shape[:2]
        rotatedPicture = np.zeros((height,width,3), picture.dtype)
        rotatedPicture = transpose(picture)
        rotatedPicture = flip(rotatedPicture, flipCode=1)

        return rotatedPicture
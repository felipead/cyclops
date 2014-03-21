class OrientationUtil:

    @staticmethod
    def findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(quadrilateral, bottomRightCorner):
        if quadrilateral.bottomLeftCorner == bottomRightCorner:
            return 3
        elif quadrilateral.topLeftCorner == bottomRightCorner:
            return 2
        elif quadrilateral.topRightCorner == bottomRightCorner:
            return 1
        elif quadrilateral.bottomRightCorner == bottomRightCorner:
            return 0
        else:
            raise Exception()

    @staticmethod
    def rotateQuadrilateralClockwiseBy90Degrees(quadrilateral, numberOfTimesToRotate):
        for i in xrange(numberOfTimesToRotate):
            quadrilateral = quadrilateral.clockwiseRotationBy90Degrees()
        return quadrilateral

    @staticmethod
    def orientQuadrilateral(quadrilateral, bottomRightCorner):
        n = OrientationUtil.findNumberOf90DegreeClockwiseRotationsToOrientQuadrilateral(quadrilateral, bottomRightCorner)
        return OrientationUtil.rotateQuadrilateralClockwiseBy90Degrees(quadrilateral, n)
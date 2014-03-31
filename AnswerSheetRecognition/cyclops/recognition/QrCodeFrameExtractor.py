from ..geometry.ConvexQuadrilateral import *
from ..geometry.Vector import *
from ..util.GeometryUtil import *
from ..util.PerspectiveUtil import *

from Frame import *

class QrCodeFrameExtractor:

    def extract(self, picture, answerSheetFrame):
        answerSheetQuadrilateral = answerSheetFrame.originalQuadrilateral.scaledBy(1.15)
        qrCodeQuadrilateral = self._extractQrCodeQuadrilateral(answerSheetQuadrilateral)
        qrCodeProjection = self._projectQuadrilateralToSquarePicture(picture, qrCodeQuadrilateral)

        frame = Frame()
        frame.originalQuadrilateral = qrCodeQuadrilateral
        frame.projectedPicture = qrCodeProjection
        return frame

    @staticmethod
    def _extractQrCodeQuadrilateral(answerSheetQuadrilateral):
        answerSheetQuadrilateral = answerSheetQuadrilateral.asClockwise()

        right = answerSheetQuadrilateral[1]
        left = answerSheetQuadrilateral[2]
        rightToLeft = Vector(left, right)

        scaledLeft = rightToLeft.multipliedByScalar(0.33).head
        scaledRight = rightToLeft.rotationBy180Degrees().multipliedByScalar(0.11).head

        qrCodeQuadrilateral = GeometryUtil.createSquareClockwiseFromTwoPoints(scaledLeft, scaledRight)
        return qrCodeQuadrilateral

    @staticmethod
    def _projectQuadrilateralToSquarePicture(picture, quadrilateral):
        counterclockwiseQuadrilateral = quadrilateral.asCounterclockwise()
        projectionSize = int(counterclockwiseQuadrilateral.largestSideLength)
        projectionSquare = ConvexQuadrilateral([(0, projectionSize-1), (0, 0), (projectionSize-1, 0), (projectionSize-1, projectionSize-1)])

        return PerspectiveUtil.projectQuadrilateralToSquarePicture(picture, counterclockwiseQuadrilateral, projectionSquare)

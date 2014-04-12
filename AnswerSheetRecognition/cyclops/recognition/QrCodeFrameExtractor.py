from ..geometry.ConvexQuadrilateral import *
from ..geometry.Vector import *
from ..util.GeometryUtil import *
from ..util.PerspectiveUtil import *

from Frame import *

class QrCodeFrameExtractor:

    __LEFT_SCALE = 0.33
    __RIGHT_SCALE = 0.11
    __ANSWER_FRAME_QUADRILATERAL_SCALE = 1.15

    def extract(self, answerFrame):
        answerFrameQuadrilateral = answerFrame.originalQuadrilateral.scaledBy(self.__ANSWER_FRAME_QUADRILATERAL_SCALE)
        qrCodeQuadrilateral = self._extractQrCodeQuadrilateral(answerFrameQuadrilateral)
        qrCodeProjection = self._projectQuadrilateralToSquarePicture(answerFrame.originalPicture, qrCodeQuadrilateral)

        frame = Frame()
        frame.originalQuadrilateral = qrCodeQuadrilateral
        frame.originalPicture = answerFrame.originalPicture
        frame.projectedPicture = qrCodeProjection
        return frame

    def _extractQrCodeQuadrilateral(self, answerFrameQuadrilateral):
        answerFrameQuadrilateral = answerFrameQuadrilateral.asClockwise()

        right = answerFrameQuadrilateral[1]
        left = answerFrameQuadrilateral[2]
        rightToLeft = Vector(left, right)

        scaledLeft = rightToLeft.multipliedByScalar(self.__LEFT_SCALE).head
        scaledRight = rightToLeft.rotationBy180Degrees().multipliedByScalar(self.__RIGHT_SCALE).head

        qrCodeQuadrilateral = GeometryUtil.createSquareClockwiseFromTwoPoints(scaledLeft, scaledRight)
        return qrCodeQuadrilateral

    @staticmethod
    def _projectQuadrilateralToSquarePicture(picture, quadrilateral):
        counterclockwiseQuadrilateral = quadrilateral.asCounterclockwise()
        projectionSize = int(counterclockwiseQuadrilateral.largestSideLength)
        projectionSquare = ConvexQuadrilateral([(0, projectionSize-1), (0, 0), (projectionSize-1, 0), (projectionSize-1, projectionSize-1)])

        return PerspectiveUtil.projectQuadrilateralToSquarePicture(picture, counterclockwiseQuadrilateral, projectionSquare)

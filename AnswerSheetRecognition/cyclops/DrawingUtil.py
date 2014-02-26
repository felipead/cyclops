from cv2 import rectangle, circle
from cv import RGB

class DrawingUtil:

    @staticmethod
    def drawRectangle(image, origin, size, rgbColor, borderSize=2):
        rectangle(image, origin, (origin[0] + size[0], origin[1] + size[1]), RGB(rgbColor[0],rgbColor[1],rgbColor[2]), borderSize)

    @staticmethod
    def drawCircle(image, center, radius, rgbColor, thickness=1):
        circle(image, center, radius, RGB(rgbColor[0],rgbColor[1],rgbColor[2]), thickness)

    @staticmethod
    def drawFilledCircle(image, center, radius, rgbColor):
        circle(image, center, radius, RGB(rgbColor[0],rgbColor[1],rgbColor[2]), thickness=-1)
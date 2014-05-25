from cv2 import rectangle, circle, polylines, line, drawContours
from cv import RGB

class DrawingUtil:

    COLOR_RED = (255,0,0)
    COLOR_GREEN = (0,255,0)
    COLOR_BLUE = (0,0,255)
    COLOR_YELLOW = (255,255,0)
    COLOR_MAGENTA = (255,0,255)
    COLOR_BLACK = (0,0,0)
    COLOR_WHITE = (255,255,255)

    @staticmethod
    def drawContour(image, contour, rgbColor, thickness=1):
        drawContours(image, [contour], 0, DrawingUtil.__toRgb(rgbColor), thickness)

    @staticmethod
    def drawFilledContour(image, contour, rgbColor):
        DrawingUtil.drawContour(image, contour, rgbColor, thickness=-1)

    @staticmethod
    def drawRectangle(image, origin, size, rgbColor, thickness=1):
        x1 = int(origin[0])
        y1 = int(origin[1])
        x2 = x1 + int(size[0])
        y2 = y1 + int(size[1])
        rectangle(image, (x1,y1), (x2,y2), DrawingUtil.__toRgb(rgbColor), thickness)

    @staticmethod
    def drawCircle(image, center, radius, rgbColor, thickness=1):
        x = int(center[0])
        y = int(center[1])
        circle(image, (x,y), int(radius), DrawingUtil.__toRgb(rgbColor), thickness)

    @staticmethod
    def drawFilledCircle(image, center, radius, rgbColor):
        DrawingUtil.drawCircle(image, center, radius, rgbColor, thickness=-1)

    @staticmethod
    def drawLine(image, point1, point2, rgbColor, thickness=1):
        x1 = int(point1[0])
        y1 = int(point1[1])
        x2 = int(point2[0])
        y2 = int(point2[1])
        line(image, (x1,y1), (x2,y2), DrawingUtil.__toRgb(rgbColor), thickness)

    @staticmethod
    def drawQuadrilateralLines(image, vertexes, rgbColor, thickness=1):
        if len(vertexes) != 4:
            raise Exception("Quadrilateral must have exactly four vertexes.")
        DrawingUtil.drawLine(image, vertexes[0], vertexes[1], rgbColor, thickness)
        DrawingUtil.drawLine(image, vertexes[1], vertexes[2], rgbColor, thickness)
        DrawingUtil.drawLine(image, vertexes[2], vertexes[3], rgbColor, thickness)
        DrawingUtil.drawLine(image, vertexes[3], vertexes[0], rgbColor, thickness)

    @staticmethod
    def __toRgb(triple):
        return RGB(triple[0],triple[1],triple[2])
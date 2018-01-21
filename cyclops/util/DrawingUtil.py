import cv2


class DrawingUtil:

    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)

    @staticmethod
    def draw_contour(image, contour, rgb_color, thickness=1):
        cv2.drawContours(image, [contour], 0, rgb_color, thickness)

    @staticmethod
    def draw_filled_contour(image, contour, rgb_color):
        DrawingUtil.draw_contour(image, contour, rgb_color, thickness=-1)

    @staticmethod
    def draw_rectangle(image, origin, size, rgb_color, thickness=1):
        x1 = int(origin[0])
        y1 = int(origin[1])
        x2 = x1 + int(size[0])
        y2 = y1 + int(size[1])
        cv2.rectangle(image, (x1, y1), (x2, y2), rgb_color, thickness)

    @staticmethod
    def draw_circle(image, center, radius, rgb_color, thickness=1):
        x = int(center[0])
        y = int(center[1])
        cv2.circle(image, (x, y), int(radius), rgb_color, thickness)

    @staticmethod
    def draw_filled_circle(image, center, radius, rgb_color):
        DrawingUtil.draw_circle(image, center, radius, rgb_color, thickness=-1)

    @staticmethod
    def draw_line(image, point1, point2, rgb_color, thickness=1):
        x1 = int(point1[0])
        y1 = int(point1[1])
        x2 = int(point2[0])
        y2 = int(point2[1])
        cv2.line(image, (x1, y1), (x2, y2), rgb_color, thickness)

    @staticmethod
    def draw_quadrilateral_lines(image, vertexes, rgb_color, thickness=1):
        if len(vertexes) != 4:
            raise Exception('Quadrilateral must have exactly four vertexes.')
        DrawingUtil.draw_line(image, vertexes[0], vertexes[1], rgb_color, thickness)
        DrawingUtil.draw_line(image, vertexes[1], vertexes[2], rgb_color, thickness)
        DrawingUtil.draw_line(image, vertexes[2], vertexes[3], rgb_color, thickness)
        DrawingUtil.draw_line(image, vertexes[3], vertexes[0], rgb_color, thickness)

import cv2
import math

CLOSE_PARAMETER = 15

class HorizontalGuideLine:
    
    def __init__(self, circles=[]):
        self._circles = circles

    def addIfClose(self, c, lists):
        for innerList in lists:
            for inner_dot in innerList:
                if abs(c[1] - inner_dot[1]) < CLOSE_PARAMETER:
                    innerList.append(c)
                    return True
        return False

    # Returns a list of dot's (x, y, radius) of the horizontal guide line.
    def recognize(self, img):

        # List of groups of dots, 
        # Where all dots are very close (CLOSE_PARAMETER) in vertical diff.
        lists = []
        for c in self._circles:
            vertical_value = c[1]
            added = self.addIfClose(c, lists)

            # Create new group for this dot.
            if (not added):
                new_list = []
                new_list.append(c)
                lists.append(new_list)

        # Foreach group, find the mean of opposite coordinate 
        meanList = []                  
        for innerList in lists:
            summ = 0
            for dot in innerList:
                summ += dot[1]
            mean = summ / len(innerList)
            meanList.append(mean)

        horizontalLineDots = lists[meanList.index(max(meanList))]
        
        # Order Dots, and draw a line from first to last.
        horizontalLineDots = sorted(horizontalLineDots, key=lambda tup: tup[0])
        first_dot = horizontalLineDots[0]
        last_dot = horizontalLineDots[len(horizontalLineDots) - 1]
        cv2.line(img, (first_dot[0], first_dot[1]), (last_dot[0], last_dot[1]), 200, 15)

        return horizontalLineDots
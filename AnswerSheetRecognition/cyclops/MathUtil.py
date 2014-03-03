from math import sqrt

class MathUtil:

    @staticmethod
    def distanceBetweenPoints(a, b):
        dx = a[0]-b[0]
        dy = a[1]-b[1]
        return sqrt( dx**2 + dy**2 )

    @staticmethod
    def equalWithinError(a, b, error):
        return abs(a - b) <= error

    @staticmethod
    def equalWithinRatio(a, b, cutRatio):
        biggest = None
        smallest = None
        if a > b:
            biggest = a
            smallest = b
        else:
            biggest = b
            smallest = a

        # avoids division by zero
        if smallest == 0:
            if biggest == 0:
                return True
            else:
                return False

        ratio = float(biggest)/float(smallest)
        
        return (ratio <= cutRatio)

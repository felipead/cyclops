from math import sqrt

class MathUtil:

    @staticmethod
    def distanceBetweenPoints(a, b):
        dx = a[0]-b[0]
        dy = a[1]-b[1]
        return sqrt( dx**2 + dy**2 )

    @staticmethod
    def isEqualsWithinError(a, b, error):
        return abs(a - b) <= abs(error)
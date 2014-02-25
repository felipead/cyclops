from math import sqrt

class MathUtil:

    @staticmethod
    def getDistanceBetween2dPoints(a, b):
        return sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

    @staticmethod
    def isEqualsWithinError(a, b, error):
        return abs(a - b) <= abs(error)
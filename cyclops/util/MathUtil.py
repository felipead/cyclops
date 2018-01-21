from math import sqrt


class MathUtil:

    @staticmethod
    def distance_between_points(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return sqrt(dx**2 + dy**2)

    @staticmethod
    def equal_within_error(a, b, error):
        return abs(a - b) <= error

    @staticmethod
    def equal_within_ratio(a, b, cut_ratio):
        largest = None
        smallest = None
        if a > b:
            largest = a
            smallest = b
        else:
            largest = b
            smallest = a

        # avoids division by zero
        if smallest == 0:
            return largest == 0

        ratio = float(largest) / float(smallest)

        return (ratio <= cut_ratio)

    @staticmethod
    def sign(x):
        if x > 0:
            return +1
        elif x == 0:
            return 0
        else:
            return -1

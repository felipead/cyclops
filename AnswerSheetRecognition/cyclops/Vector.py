import math

class Vector(tuple):
    def __init__(self, point):
        tuple.__init__(self,point)

    @classmethod
    def create(_class, point, origin):
        value = []
        for i in xrange(len(point)):
            value.append(point[i] - origin[i])
        return Vector(value)

    def innerProduct(self, anotherVector):
        sum = 0
        for i, j in zip(self, anotherVector):
            sum += i * j
        return sum

    def norm(self):
        sum = 0
        for i in self:
            sum += i*i
        return math.sqrt(sum)

    def angleBetween(self, anotherVector):
        v = self
        w = anotherVector

        return math.acos( v.innerProduct(w) / (v.norm() * w.norm()) )
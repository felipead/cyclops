class PatternMatch:

    def __init__(self, location, size):
        self.location = location
        self.size = size

    @property
    def center(self):
        x = self.location[0] + (self.size[0]/2)
        y = self.location[1] + (self.size[1]/2)
        return (x, y)

    @classmethod
    def from_center(_class, center, size):
        x = center[0] - size[0]/2
        y = center[1] - size[1]/2
        return PatternMatch((x,y), size)

    def __str__(self):
        return str(self.center)

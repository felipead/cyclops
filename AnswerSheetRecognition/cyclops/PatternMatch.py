class PatternMatch:

    def __init__(self, location, size):
        self.location = location
        self.size = size

    def getCenter(self):
        x = self.location[0] + (self.size[0]/2)
        y = self.location[1] + (self.size[1]/2)
        return (x, y)
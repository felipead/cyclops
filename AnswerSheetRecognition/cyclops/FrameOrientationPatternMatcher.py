from AbstractPatternMatcher import *

class FrameOrientationPatternMatcher(AbstractPatternMatcher):
    
    def __init__(self):
        super(FrameOrientationPatternMatcher,self).__init__("FrameOrientation", [30, 45])
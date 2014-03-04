from AbstractPatternMatcher import *

class QrCodeEdgePatternMatcher(AbstractPatternMatcher):
    
    def __init__(self):
        super(QrCodeEdgePatternMatcher,self).__init__("QrCodeEdge", [32, 48])
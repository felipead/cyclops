from cv2 import *

from AnswerSheetRecognizer import *

namedWindow("preview")
camera = VideoCapture(0)

_, picture = camera.read()

while True:

    if picture is not None:
        recognizer = AnswerSheetRecognizer()
        recognizer.recognize(picture)
        imshow("preview", picture)
    
    _, picture = camera.read()

    if waitKey(1) & 0xFF == ord('q'):
        break
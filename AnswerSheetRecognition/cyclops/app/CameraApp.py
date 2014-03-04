from cv2 import *

from ..recognition.AnswerSheetRecognizer import *

WINDOW_NAME = "preview"

def readCamera(camera):
    _, picture = camera.read()
    picture = flip(picture, 1);
    return picture


def execute():
    namedWindow(WINDOW_NAME)
    camera = VideoCapture(0)

    picture = readCamera(camera)

    while True:

        if picture is not None:
            recognizer = AnswerSheetRecognizer()
            recognizer.recognize(picture)
            imshow(WINDOW_NAME, picture)
        
        picture = readCamera(camera)

        if waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    execute()
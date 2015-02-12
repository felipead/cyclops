from cv2 import waitKey, VideoCapture

from AnswerSheetRecognitionController import *

def readCamera(camera):
    _, picture = camera.read()
    return picture

def exitKeyPressed():
    return waitKey(1) & 0xFF == ord('q')

def execute():
    camera = VideoCapture(0)
    controller = AnswerSheetRecognitionController()
    controller.init()

    picture = readCamera(camera)
    while True:
        if picture != None:
            controller.processPicture(picture)
        picture = readCamera(camera)
        if exitKeyPressed():
            break

if __name__ == "__main__":
    execute()
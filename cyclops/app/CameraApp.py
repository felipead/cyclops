import cv2

from .AnswerSheetRecognitionController import *

def read_camera(camera):
    _, picture = camera.read()
    return picture

def exit_key_pressed():
    return cv2.waitKey(1) & 0xFF == ord('q')

def execute():
    camera = cv2.VideoCapture(0)
    controller = AnswerSheetRecognitionController()
    controller.init()

    picture = read_camera(camera)
    while True:
        if picture is not None:
            controller.process_picture(picture)
        picture = read_camera(camera)
        if exit_key_pressed():
            break

if __name__ == '__main__':
    execute()

#!/usr/bin/env python
from flask import Flask
from flask_restful import Api, Resource
#import cv2
import sys
import threading
import os

# Server constants
app = Flask(__name__)
api = Api(app)

# Constants
"""DEVICE_NUMBER = 0
FONT_FACES = [
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_COMPLEX_SMALL,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX
]"""

#region Camera Thread
class CameraThread(threading.Thread):
    #faceCascade = cv2.CascadeClassifier('cars.xml')
    #vc = cv2.VideoCapture(DEVICE_NUMBER)
    i = 0
    faces = []
    cars = 0
    DEVICE_NUMBER = 0

    def getLatestCarsDetected(self):
        return self.cars

    def getDeviceNumer(self):
        return self.DEVICE_NUMBER

    def run(self):
        print 'Running thread'

        while True:
            if self.i % 5 == 0:
                """if self.vc.isOpened():  # try to get the first frame
                    # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-read
                    retval, frame = self.vc.read()
                else:
                    # Exit the program
                    break

                frame_show = frame

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(
                    frame,
                    scaleFactor=1.2,
                    minNeighbors=2,
                    minSize=(50, 50),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

                cv2.imshow('frame', frame)

                print len(faces)
                cars = len(faces)"""

                self.cars += 1

            self.i += 1

    def __init__(self, DEVICE_NUMBER=0):
        super(CameraThread, self).__init__()
        self.DEVICE_NUMBER = DEVICE_NUMBER
        self.start()
#endregion

#region AvailableLots
class AvailableLots(Resource):

    cameraThread = CameraThread(DEVICE_NUMBER=0)
    cameraThread2 = CameraThread(DEVICE_NUMBER=1)

    def get(self):
        return {
            'available1': self.cameraThread.getLatestCarsDetected(),
            'device1': self.cameraThread.getDeviceNumer(),
            'available2': self.cameraThread2.getLatestCarsDetected(),
            'device2': self.cameraThread2.getDeviceNumer()
        }
#endregion

# Actually setup the Api resource routing here
api.add_resource(AvailableLots, '/available')

if __name__ == '__main__':
    app.run(debug=True)

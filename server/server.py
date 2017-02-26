#!/usr/bin/env python
from flask import Flask
from flask_restful import Api, Resource
import cv2, threading
import requests



# Server constants
app = Flask(__name__)
api = Api(app)


# region Thread
class CameraThread(threading.Thread):
    # Constants
    DEVICE_NUMBER = 0
    FONT_FACES = [
        cv2.FONT_HERSHEY_SIMPLEX,
        cv2.FONT_HERSHEY_PLAIN,
        cv2.FONT_HERSHEY_DUPLEX,
        cv2.FONT_HERSHEY_COMPLEX,
        cv2.FONT_HERSHEY_TRIPLEX,
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    ]
    faceCascade = cv2.CascadeClassifier('cars.xml')
    vc = cv2.VideoCapture(DEVICE_NUMBER)
    i = 0
    tem = 0

    def getAvailableLots(self):
        return self.tem

    def run(self):
        if not self.vc.isOpened():  # try to get the first frame
            # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-read
            return -1
        else:
            retval, frame = self.vc.read()

            while True:
                suma = 0

                frame_show = frame
                if self.i % 5 == 0:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.faceCascade.detectMultiScale(
                        frame,
                        scaleFactor=1.2,
                        minNeighbors=2,
                        minSize=(50, 50),
                        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                    )
                if self.tem != len(faces):
                    print len(faces)
                    self.tem = len(faces)
                    r=requests.post("https://super-parking.herokuapp.com/available/"+str(self.tem))
                    print r

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame_show, (x, y), (x + w, y + h), (0, 0, 255), 2)

                retval, frame = self.vc.read()

                self.i += 1

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(CameraThread, self).__init__(group, target, name, args, kwargs, verbose)
        self.start()


# endregion

cThread = CameraThread()

# region AvailableLots
class AvailableLots(Resource):
    def get(self):
        return {
            'available': cThread.getAvailableLots() < 4
        }


# endregion


# Actually setup the Api resource routing here
api.add_resource(AvailableLots, '/available')

if __name__ == '__main__':
    app.run(host='10.33.1.250', port=8080)

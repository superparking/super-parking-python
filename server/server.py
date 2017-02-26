#!/usr/bin/env python
from flask import Flask
from flask_restful import Api, Resource
import cv2

# Server constants
app = Flask(__name__)
api = Api(app)

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


# region AvailableLots
class AvailableLots(Resource):
    faceCascade = cv2.CascadeClassifier('cars.xml')
    vc = cv2.VideoCapture(DEVICE_NUMBER)
    i = 0

    def getLots(self):
        if not self.vc.isOpened():  # try to get the first frame
            # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-read
            return 0
        else:
            suma = 0

            for x in range(0, 5):
                retval, frame = self.vc.read()
                # Exit the program

                frame_show = frame

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(
                    frame,
                    scaleFactor=10,
                    minNeighbors=1,
                    minSize=(5, 5),
                    maxSize=(5, 10),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

                print 'Cars: ' + str(len(faces))
                suma += len(faces)

            return (suma / 5)

    def get(self):
        return {
            'available': self.getLots()
        }  # endregion


# Actually setup the Api resource routing here
api.add_resource(AvailableLots, '/available')

if __name__ == '__main__':
    app.run(debug=True)

#!/usr/bin/env python
import cv2, sys
import os
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

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

# Server constants
app = Flask(__name__)
api = Api(app)


# AvailableLots
class AvailableLots(Resource):
    def get(self):
    	vd = Vehicledetect()

    	cars = vd.get()
	print 'Cars:' + str(cars)

        return {
        	'available': cars
        }

# Detect Vehicles n stuff
class Vehicledetect():

	# Get the number of cars in parking lot
	def get(self):
#if len(sys.argv) > 1:
#	XML_PATH = sys.argv[1]
#else:
#	print "Error: XM path not defined"
#	sys.exit(1)

		faceCascade = cv2.CascadeClassifier('cars.xml')

# Init webcam
# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-videocapture
		vc = cv2.VideoCapture(DEVICE_NUMBER)

		# Check if the webcam init was successful
		# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-isopened

		if vc.isOpened(): # try to get the first frame
		    # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-read
		    retval, frame = vc.read()
		else:
		    # Exit the program
		    return -1

		i = 0
		faces = []

		while True:
			frame_show = frame
			if i % 5 == 0:
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				faces = faceCascade.detectMultiScale(
					frame,
					scaleFactor=1.2,
					minNeighbors=2,
					minSize=(50, 50),
					flags=cv2.cv.CV_HAAR_SCALE_IMAGE
				)

				cv2.imshow('frame', frame)

				print len(faces)	
				return len(faces)

			i+=1

##
## Actually setup the Api resource routing here
##
api.add_resource(AvailableLots, '/available')


if __name__ == '__main__':
    app.run(debug=True)

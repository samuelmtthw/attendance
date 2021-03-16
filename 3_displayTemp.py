# import packages
from imutils.video import VideoStream
from imutis.video import FPS
import argparse
import imutils
import time
import cv2
import os
import board
import busio as io
import adafruit_mlx90614


# load OpenCV's Haar cascade for face detection from disk
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# creating connection to MLX90614
i2c = io.I2C(board.SCL, board.SDA, frequency = 100000)
mlx = adafruit_mlx90614.MLX90614(i2c)


# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")

# use this if you are using webcam
# vs = VideoStream(src=0).start()

# use this if you are using piCam
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    # getting temperature from MLX90614
    objectTemp = "{:.2f}".format(mlx.object_temperature)
    
    # convert the input frame from (1) BGR to grayscale (for face
    # detection) and (2) from BGR to RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # loop over the face detections and draw them on the frame
    # also put the temperature
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, objectTemp, (x, y + h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

#stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()



# USAGE
# 6_faceRecognition_DB.py --encodings encodings.pickle

# import face recognition packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

# import database packages
import mysql.connector
import datetime
import argparse

# construct the argument parser & parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

# load the known faces + embeddings and Haar's cascade
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# create connection to the database
#! change the host depends on the device you are using
print("[INFO] connecting to the database...")
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root", 
    database = "attendance_system"
)
myCursor = db.cursor()

# set current date
print("[INFO] loading data from the database")
now = datetime.datetime.now()
currentDate = now.strftime("%Y-%m-%d")

# get all of the employeeID from the database
sql = "SELECT employeeID FROM employee"
myCursor.execute(sql)
employees = myCursor.fetchall()

# create a dictionary to count how many times the ID is already detected today
timesDetected = {}
for employee in employees:
    timesDetected[employee[0]] = 0

# create a list for finished IDs
todayFinish = []

# get all of the finished IDs from today's attendance list
sql = "SELECT employeeID from attendance_list WHERE attendanceDate = %s AND finishTime IS NOT NULL"
val = (currentDate,)
myCursor.execute(sql, val)
finished = myCursor.fetchall()

for result in finished:
    todayFinish.append(result[0])

# initialize video stream and warm up the camera
#! change the VideoStream source depends on the camera you are using
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start() # for webcam
# vs = VideoStream(usePiCamera=True).start() # for picamera
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True: 
    # set current time
    currentTime = now.strftime("%H:%M:%S")

    # get all of the IDs from today's attendance list from the database
    sql = "SELECT employeeID FROM attendance_list WHERE attendanceDate = %s"
    val = (currentDate,)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()

    # create a list for present IDs
    todayStart = []

    # put all of the present IDs into the list
    for result in myResult:
        todayStart.append(result[0])

    # grab the frame from the threaded video stream and resize it to 500px (to speedup processing)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    #! delete later!
    objectTemp = 36.8

    # convert the BGR input frame to: 
    # (1) grayscale (for face detection) 
    # (2) RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame 
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(200, 200), flags=cv2.CASCADE_SCALE_IMAGE)

    # reordering the coordinates from (x,y,w,h) from OpenCV to (top, right, bottom, left)
    boxes = [(y, x+w, y+h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then
            # initialize a dictionary to count the total number
            # of times each face was matched
            matchedIdxs = [i for (i,b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for 
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie 
            # Python will select first entry in the dictionary)
            name = max(counts, key=counts.get)

            # wait for the faces to reach certain number 
            timesDetected[name] += 1
            print(timesDetected)

            # loop over the dictionary
            for employeeID in timesDetected:
                # check if there is a face that already reach the required number
                #! change the number based on the time you get for 5 seconds
                if timesDetected[employeeID] > 100:
                    # check if the ID is already present
                    if employeeID in todayStart:
                        # check if the ID is already gone
                        if employeeID not in todayFinish:
                            # if the ID is not gone, update the entry in the database
                            sql = "UPDATE attendance_list SET finishTime = %s, finishTemp = %s WHERE attendanceDate = %s AND employeeID = %s"
                            val = (currentTime, objectTemp, currentDate, employeeID)
                            myCursor.execute(sql, val)
                            db.commit()

                            print("Entry updated")

                            # reset the counter of that ID
                            timesDetected[name] = 0

                            # add the ID to the finished list
                            todayFinish.append(name)
                        
                        else:
                            timesDetected[name] = 0

                    else:
                        sql = "INSERT INTO attendance_list (employeeID, attendanceDate, startTime, startTemp) VALUES (%s, %s, %s, %s)"
                        val = (name, currentDate, currentTime, objectTemp)
                        myCursor.execute(sql, val)
                        db.commit()      

                        print("New entry added")

                        # reset the counter for that ID
                        timesDetected[name] = 0

        # update the list of names
        names.append(name)
    
    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # display the image to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
		
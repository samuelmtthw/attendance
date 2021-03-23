# USAGE
# python3 face2DB.py -f "papi/mami/koko/dede" -d "raspberry/mac" -ip "youripaddress"

# import the necessary packages
import mysql.connector
import datetime
import argparse

# construct the argument parser & parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument ("-f", "--face", required=True,
    help = "the id of the detected face")
ap.add_argument ("-d", "--device", required=True,
    help = "the device that you are using")
ap.add_argument ("-ip", "--ip", default="localhost", 
    help = "ip address of the database")

args = vars(ap.parse_args())

# create object Person
class Person:
    def __init__(self, id, temp):
        self.id = id
        self.temp = temp

# create 4 Person objects
face1 = Person("0321001", 36)
face2 = Person("0321002", 37)
face3 = Person("0321003", 38)
face4 = Person("0321004", 39)

# select the type of connection based on the device
if args["device"]=="raspberry":
    db = mysql.connector.connect(
        host = args["ip"],
        user = "root",
        password = "root",
        database = "attendance_system"
    )
elif args["device"]=="mac":
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "attendance_system"
    )

mycursor = db.cursor()


# set status
tempDetected = True

# select current face and print it on the console
if args["face"]=="papi":
    currentFace = face1
elif args["face"]=="mami":
    currentFace = face2
elif args["face"]=="koko":
    currentFace = face3
elif args["face"]=="dede":
    currentFace = face4
print("ID =", currentFace.id)


if tempDetected == True:
  # get current date & time
  now = datetime.datetime.now()
  currentDate = now.strftime("%Y-%m-%d")
  currentTime = now.strftime("%H:%M:%S")
  
  # assume that the person is not present today
  present = False

  # take all of the data from today's attendance list
  sql = "SELECT attendanceID, employeeID, startTime, finishTime FROM attendance_list WHERE attendanceDate = %s"
  val = (currentDate,)
  mycursor.execute(sql,val)
  myresult = mycursor.fetchall()


  # loop over the result
  for x in myresult:

    # if the detected face is already present today, set "present = True" and print it on the console
    if x[1] == currentFace.id:
      present = True
      print("The Employee is present today")

      # insert the current time into errorTime
      sql = "UPDATE attendance_list SET errorTime = %s WHERE attendanceID = %s"
      val = (currentTime, x[0])
      mycursor.execute(sql,val)
      db.commit()
      print("errorTime added")

      # get the startTime and errorTime
      sql = "SELECT startTime, errorTime FROM attendance_list WHERE attendanceID = %s"
      val = (x[0], )
      mycursor.execute(sql,val)
      times = mycursor.fetchall()
      startTime, errorTime = times[0]
    
      # check the time difference
      #! change the time difference here
      minTime = datetime.timedelta(seconds=10)
      timeDiff = errorTime-startTime

      # end the program if the time difference is not satisfied
      if timeDiff < minTime:
        #! don't forget to change the warning
        print("Please wait for 10 seconds to add new record")
        break
    
      # if the employee hasn't go home, insert finishTime and finishTemp
      if x[3] == None:
        sql = "UPDATE attendance_list SET finishTime = %s, finishTemp = %s WHERE attendanceID = %s"
        val = (currentTime, currentFace.temp, x[0])
        mycursor.execute(sql,val)
        db.commit()
        print("Attendance updated")
        
        sql = "UPDATE attendance_list SET errorTime = NULL WHERE attendanceID = %s"
        val = (x[0],)
        mycursor.execute(sql,val)
        db.commit()
        print("errorTime removed")

  
  # if the employee is not present today, add a new record to the database
  if present == False:
    sql = "INSERT INTO attendance_list (employeeID, attendanceDate, startTime, startTemp) VALUES (%s,%s,%s,%s)"
    val = (currentFace.id, currentDate, currentTime, currentFace.temp)
    mycursor.execute(sql, val)
    db.commit()
    print("New attendance added")
      
print("Program ended")
print("-----------------------")


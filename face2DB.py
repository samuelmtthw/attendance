#RUN WITH:
#python3 face2DB.py -f "papi/mami/koko/dede" -d "raspberry/mac" -ip "ipaddress"

#LIBRARIES
import mysql.connector
import datetime
import argparse

#ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument ("-f", "--face", required=True,
    help = "the id of the detected face")
ap.add_argument ("-d", "--device", required=True,
    help = "the device that you are using")
ap.add_argument ("-ip", "--ip", default="localhost", 
    help = "ip address of the database")

args = vars(ap.parse_args())

#SET FACE
class Person:
    def __init__(self, id, temp):
        self.id = id
        self.temp = temp

face1 = Person("0321001", 36)
face2 = Person("0321002", 37)
face3 = Person("0321003", 38)
face4 = Person("0321004", 39)


if args["device"]=="raspberry":
    #! SET DATABASE (RASPBERRY PI TO MAC)
    # change the host's IP address according to Macbook's IP addres.
    db = mysql.connector.connect(
        host = args["ip"],
        user = "root",
        password = "root",
        database = "attendance_system"
    )
elif args["device"]=="mac":
    #SET DATABASE (LOCAL MACHINE)
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "attendance_system"
    )

mycursor = db.cursor()


#SET STATUS
tempDetected = True

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
  
  #AMBIL WAKTU SEKARANG
  now = datetime.datetime.now()
  currentDate = now.strftime("%Y-%m-%d")
  currentTime = now.strftime("%H:%M:%S")
  

  #HARI INI MASUK?
  present = False

  #AMBIL DATA SEMUA ORANG YANG MASUK HARI INI
  sql = "SELECT attendanceID, employeeID, startTime, finishTime FROM attendance_list WHERE attendanceDate = %s"
  val = (currentDate,)
  mycursor.execute(sql,val)
  myresult = mycursor.fetchall()


  #CHECK YANG DATENG HARI INI SIAPA AJA
  for x in myresult:

    #KALO MUKA YANG KEDETECT UDAH ADA DI DATABASE (UDAH ABSEN HARI INI), 
    if x[1] == currentFace.id:
      present = True
      print("The Employee is present today")

      #INPUT WAKTU SEKARANG KE errorTime
      sql = "UPDATE attendance_list SET errorTime = %s WHERE attendanceID = %s"
      val = (currentTime, x[0])
      mycursor.execute(sql,val)
      db.commit()
      print("errorTime added")

      #CHECK APAKAH JEM MASUK DIA (startTime) < 5 MENIT DARI JAM SEKARANG (errorTime)
      sql = "SELECT startTime, errorTime FROM attendance_list WHERE attendanceID = %s"
      val = (x[0], )
      mycursor.execute(sql,val)
      times = mycursor.fetchall()

      startTime, errorTime = times[0]
      #! change the time difference here
      minTime = datetime.timedelta(seconds=10)
      timeDiff = errorTime-startTime

      if timeDiff < minTime:
        #! don't forget to change the warning
        print("Please wait for 10 seconds to add new record")
        break
    
      #CHECK APAKAH DIA UDAH ABSEN PULANG. JIKA BELUM, KITA UPDATE RECORD PAS DIA MASUK DAN MASUKIN finishTime + finishTemp
      if x[3] == None:
        #UPDATE OLD ATTENDANCE (FINISH)
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

  
  #KALO HARI INI BELOM DATENG, BIKIN RECORD BARU. MASUKIN employeeID, date, startTime, startTemp dari hasil pembacaan kamera
  if present == False:
    #INSERT NEW ATTENDANCE (START)
    sql = "INSERT INTO attendance_list (employeeID, attendanceDate, startTime, startTemp) VALUES (%s,%s,%s,%s)"
    val = (currentFace.id, currentDate, currentTime, currentFace.temp)
    mycursor.execute(sql, val)
    db.commit()
    print("New attendance added")
      
print("Program ended")
print("-----------------------")


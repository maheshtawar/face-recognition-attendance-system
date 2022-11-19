import pyautogui
from base64 import encode
import cv2
import numpy
import face_recognition
import os
import pymysql
from datetime import datetime,date

class FaceRecognition:    
    def __init__(self,sub):
        # sub = input("Enter subject Name:")
        atd = []
        path = 'images'
        images = []
        personName = []
        myList = os.listdir(path)
        # print(myList)
        for curr_img in myList:
            current_img = cv2.imread(f'{path}/{curr_img}')
            images.append(current_img)
            personName.append(os.path.splitext(curr_img)[0])
        # print(personName)

        def attendance(name):
            rollNo = name.split('_')[0]
            s_name = name.split('_')[1]
            con = pymysql.connect(host='localhost',user='root',password='',database='face_recognition')
            cur = con.cursor()
            cur.execute("SELECT * from attendance where date = %s and subject = %s",(date.today(),sub))
            rollList = []
            for row in cur:
                rollList.append(row[1])
            if rollNo not in rollList:
                cur.execute("""INSERT INTO attendance(roll_no,fname,subject) VALUES(%s,%s,%s)""", (rollNo,s_name,sub))
                print("Added to database")
                # pyautogui.alert("Attendance Marked Successfully")
            else:
                print("Already Exist")     
                # pyautogui.alert("Attendance Already Exist")
    
            con.commit()

        def faceEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)   # cv2 return images in BGR format so we convert it to RGB
                encode = face_recognition.face_encodings(img)[0]    # an image, return the 128-dimension face encoding (128 unique points of face) for each face in the image.
                encodeList.append(encode)
            return encodeList

        encodeListKnown = faceEncodings(images)
        print("Encoding Done !!!")

        cam = cv2.VideoCapture(0)   # to capture video, if laptop camera parameter is 0 or for external webcam parameter is 1

        while True:
            ret,frame = cam.read()
            faces = cv2.resize(frame,(0,0),None,0.25,0.25)
            faces = cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(faces)
            face_encodings = face_recognition.face_encodings(faces,face_locations)

            for encodeFace,faceLoc in zip(face_encodings,face_locations):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

                matchIndex = numpy.argmin(faceDis)
                s_name = "Unknown"
                face_names = []

                if matches[matchIndex]:
                    name = personName[matchIndex]
                    rollNo = name.split('_')[0]
                    s_name = name.split('_')[1]
                face_names.append(s_name)
                if s_name not in atd:
                    if s_name!="Unknown":
                        atd.append(s_name)
                        attendance(name)
                
                for (y1, x2, y2, x1), name in zip(face_locations, face_names):
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)    
                    cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                    cv2.putText(frame,s_name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    
                
            cv2.imshow("Camera/Press Enter to Exit",frame)
            if cv2.waitKey(10) == 13:   #value of Enter key is 13
                break
        cam.release()
        cv2.destroyAllWindows()    


if __name__ == "__main__":
    sub = input("Enter Subject : ")
    FaceRecognition(sub)
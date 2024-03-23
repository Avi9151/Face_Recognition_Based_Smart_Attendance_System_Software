from sklearn.neighbors import KNeighborsClassifier

import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime

# from win32com.client import Dispatch
# def speak(str1):
#     speak = Dispatch(("SAPI.SpVoice"))
#     speak.speak(str1)

import pyttsx3
# Men voice-----------

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait() 

# female voice---------

# def speak(text):
#     engine = pyttsx3.init()
#     engine.setProperty('voice', 'english+f3')
#     engine.say(text)
#     engine.runAndWait()


video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('Data/haarcascade_frontalface_default.xml')

with open('Data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)
    
with open('Data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("bg1.png")

COL_NAMES = ['NAME', 'TIME']

while True:
    ret, frame = video.read()
    # frame = cv2.resize(frame, (500,400))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50,50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist = os.path.isfile("Attendance/Attendance_"+ date +".csv")
        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x,y-40), (x+w, y), (50, 50, 255), -1)        
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)       
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50, 50, 255), 1)
        attendance = [str(output[0]), str(timestamp)]
    imgBackground[162:162+480, 55:55+640] = frame
    
    cv2.imshow("Frame", imgBackground )
    k = cv2.waitKey(1)
    if k == ord('o'):
        speak("Attendance Marked")
        time.sleep(5)
            
        if exist:
            with open("Attendance/Attendance_"+ date +".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance/Attendance_"+ date +".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    if k == ord('q'):
        break   
video.release() 
cv2.destroyAllWindows()
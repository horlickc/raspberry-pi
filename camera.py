import numpy as np
import cv2
import os
import pickle
from gtts import gTTS
from playsound import playsound
import time
#from _datetime import datetime
import pygame
from pygame.locals import *


face_cascade = cv2. CascadeClassifier('./faces/cascades/data/haarcascade_frontalface_alt2.xml')
recon = cv2.face.LBPHFaceRecognizer_create()
recon.read("./recognizers/trianed_data.yml")
#print(recon.read("./recognizers/trianed_data.yml"))

labels = {"name": 1}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 247, 0), 2) #draw rectangle when faces are detected
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        id, conf = recon.predict(roi_gray)
        if conf>=45 and conf<=85:
            # print(id)
            print(labels[id])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id]
            cv2.putText(img, name, (x,y), font, 1, (255, 247, 0), 2, cv2.LINE_AA)

            # print(x, y, w, h)
            sentence = "Reminder... " + str(name) + " is waiting for you."
            tts = gTTS(text=sentence, lang="en")
            tts.save("./sounds/speech.mp3")
            time.sleep(1)

            pygame.mixer.init()
            pygame.mixer.music.load("./sounds/speech.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue


        #img_item = str(datetime.now()).replace(":", "-") + ".jpg"
        img_item = "faces.jpg"
        print(img_item)
        cv2.imwrite(img_item, roi_color)

    cv2.imshow('img', img)
        #playsound("./sounds/speech.mp3")
    # open1 = open("./sounds/speech.mp3")
    # open1.close()
    k = cv2.waitKey(30) & 0xff #hit esc to kill the program
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

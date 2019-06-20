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
import speech_recognition as sr
from PIL import Image
import os
import email
import imaplib
import pywapi
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path



def train_faces():
    print("Initializing...\n")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "faces/image")

    face_cascade = cv2. CascadeClassifier('./faces/cascades/data/haarcascade_frontalface_alt2.xml')
    recon = cv2.face.LBPHFaceRecognizer_create()
    

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []
    print("Done initialized.\nTraining...\n")
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg") or file.endswith("JPG"):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace(" ", "-").lower()
                print(label, path)
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id = label_ids[label]
                # print(label_ids)
                # y_labels.append(label)
                # x_train.append(path)
                pil_image = Image.open(path).convert("L")
                size = (550, 550)
                final_image = pil_image.resize(size, Image.ANTIALIAS)
                image_array = np.array(final_image, "uint8")
                # print(image_array)
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                for (x,y,w,h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_labels.append(id)

    # print(y_labels)
    # print(x_train)

    with open("labels.pickle", "wb") as f:
        pickle.dump(label_ids, f)

    recon.train(x_train, np.array(y_labels))
    recon.write("recognizers/trianed_data.yml")
    print("\nComplete.")
    menu("You are now back to menu")

def open_camera():
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

            else:
                email_alert()


            #img_item = str(datetime.now()).replace(":", "-") + ".jpg"
            img_item = "faces.jpg"
            print(img_item)
            cv2.imwrite(img_item, roi_color)

        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff #hit esc to kill the program
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("--------------------------------")
    menu("You are now back to menu")

def voice():
    while 1:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Waiting for command")
            #playsound("./sounds/listening.mp3")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
            command_list(command)
            

        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('Your last command couldn\'t be heard. Please input command through text')
            alt = raw_input('command: ')
            command_list(alt.lower())
            print("--------------------------------")
            command = menu("You are now back to menu");

        return command

def command_list(cm):
    if cm == "email":
        #print("gg")
        username = "tobychan98.w@gmail.com"
        password = "ZwFMwNTeehyL9aGR"

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)

        mail.select("inbox")
        # result, data = mail.uid("search", None, "ALL")

        (retcode, messages) = mail.search(None, "(UNSEEN)")

        list = messages[0].split()
        list_len = len(list)

        sentence = ("You have " + str(list_len) + "E-mails unread......")
        tts = gTTS(text=sentence, lang="en")
        tts.save("./sounds/email_speech.mp3")
        time.sleep(1)

        pygame.mixer.init()
        pygame.mixer.music.load("./sounds/email_speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        menu("You are now back to menu")

    elif cm == "weather":
        query = pywapi.get_weather_from_weather_com("HKXX0523")

        temperature = query['current_conditions']['temperature']
        humidity = query['current_conditions']['humidity']

        sentence = ("Today's temperature is " + str(temperature) + " degree celsius, the humidity is " + str(humidity) + "percent......")
        tts = gTTS(text=sentence, lang="en")
        tts.save("./sounds/weather_speech.mp3")
        time.sleep(1)

        pygame.mixer.init()
        pygame.mixer.music.load("./sounds/weather_speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        menu("You are now back to menu")

    else:
        print("No matched command. Back to menu\n")
        menu("You are now back to menu")

def email_alert():
    email = 'tobychan98.w@gmail.com'
    password = 'ZwFMwNTeehyL9aGR'
    send_to_email = 'tobychan98.w@gmail.com'
    subject = 'Unrecognize faces'
    message = '<p>Greetings to you. </p><p>There is an unrecognized face outside the apartment. Is that somebody you know? </p><p>Click <a href="http://0.0.0.0:5000">here</a> to view.</p>'
    file_location = '/home/pi/Downloads/mine/faces.jpg'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'html'))
    
    with open('/home/pi/Downloads/mine/faces.jpg', 'rb') as f:
        mime = MIMEBase('image', 'jpg', filename='faces.jpg')
        mime.add_header('This is the unrecogonized face', 'attachment', filename='faces.jpg')
        #mime.add_header('X-Attachment-Id', '0')
        #mime.add_header('Content-ID', '<0>')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)
    
    #filename = os.path.basename(file_location)
    #attachment = open(file_location, "rb")
    #part = MIMEBase('application', 'octet-stream')
    #part.set_payload(attachment.read())
    #encoders.encode_base64(part)
    #part.add_header('This is the unrecognized face', "attachment", filename= "%s" % filename)
    #msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

def menu(status):
    if status == "":
        print("Welcome to SMART HOME ASSISTANT\n Please enter number to proceed")
    else:
        print(status)
    print("--------------------------------")
    print("1. Update facial recognition")
    print("2. Open facial recognition")
    print("3. Commands")
    print("--------------------------------")
    print("Press Q to quit.")
    choice = raw_input("Choice: ")
    print("--------------------------------")
    if choice == "1":
        train_faces()
    elif choice == "2":
        open_camera()
    elif choice == "3":
        voice()
    elif choice == "q":
        quit()
    #print(choice)
    

if __name__ == '__main__':
    menu("")

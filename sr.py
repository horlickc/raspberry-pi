import speech_recognition as sr

def talk(audio):
    #"speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def myCommand():
    #"listens for commands"

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

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard. Please input command through text')
        alt = raw_input('command: ')
        print(alt)
        command = myCommand();

    return command

while True:
    myCommand()

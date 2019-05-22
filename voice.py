from gtts import gTTS
import time
from pydub import AudioSegment

# Passing the text and language to the engine
tts = gTTS(text="I am listening. I am listening. ", lang="en", slow=True) 

# Saving the converted audio in a wav file named sample
tts.save('./sounds/sample.mp3')

#time.sleep(1)

#sound = AudioSegment.from_mp3("./sounds/sample.mp3")
#sound.export("./sounds/sample.wav", format="wav")
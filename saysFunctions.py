from gtts import gTTS
from playsound import playsound 
import os

def say_text(text):
    tts = gTTS(text, lang = "ru",slow=False)
    tts.save("test.mp3")
    playsound("test.mp3") 
    os.remove("test.mp3")

import sys
import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()
def start_listening():

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    stop_listening = recognizer.listen_in_background(microphone, handle_audio)
        


def handle_audio(recognizer, audio):
    try:
        print("U can say")
        #check.my_function()
        recognized_text = recognizer.recognize_google(audio, language = "ru-RU")
        print('You said: ' + recognized_text)
        print("End")
    except sr.UnknownValueError:
        print('Could not understand audio')
    except sr.RequestError as e:
        print('Error: ' + str(e))

if __name__ == '__main__':
    start_listening()
    handle_audio()

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor,QKeySequence
import speech_recognition as sr
from playsound import playsound 
from commandFile import handle
from saysFunctions import say_text
import keyboard
import pyaudio
import vosk
import json
import threading
recognizer = sr.Recognizer()
microphone = sr.Microphone()
mic = sr.Microphone()
# параметры для настроек
hot_word = 'алина'
phrase_time_limit_hotword = 3
phrase_time_limit_command= 5
dynamic_threshold = True
energy_threshold = 300
pause_threshold = 0.8
# использование параметров
recognizer.dynamic_energy_threshold = dynamic_threshold
recognizer.energy_threshold = energy_threshold
recognizer.pause_threshold = pause_threshold
stop_listening = None
recognizerType = "Vosk"
commandrecognizerType = "Vosk"

model_path = "model_small"  # Укажите путь к модели Vosk
model = vosk.Model(model_path)

# Создание объекта распознавания
rec = vosk.KaldiRecognizer(model, 16000)



def create_launch_program_widget():
    # создаем виджет с кнопкой для запуска программы
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignCenter)
    upBox = QVBoxLayout()
    upBox.setAlignment(Qt.AlignCenter)
    downBox = QVBoxLayout()

    btn_launch_program = QPushButton("Start", widget)
    gradient_style = "QPushButton {border-radius: 150px;padding: 5px;\
                  background: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, \
                  stop:0 #492989, stop:1 #5e35b1);color: #fff;font-size: 26px;font-weight: bold;} \
                  QPushButton:hover {border-radius: 150px;background: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, \
                  stop:0 #691b7e, stop:1 #8e24aa);} \
                  QPushButton:pressed {border-radius: 150px;background: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, \
                  stop:0 #6a1b9a, stop:1 #4a148c);}"

    btn_launch_program.setStyleSheet(gradient_style)
    btn_launch_program.setFixedSize(300, 300)
    shadow = QGraphicsDropShadowEffect(blurRadius=100, xOffset=0, yOffset=0)
    #shadow.setColor(QColor(128, 0, 128))
    #shadow.setColor(QColor(255, 255, 255))
    #btn_launch_program.setGraphicsEffect(shadow)
    upBox.addWidget(btn_launch_program)

    
    # добавляем список для вывода сообщений
    list_widget = QListWidget(widget)
    list_widget.setMaximumHeight(100)
    list_widget.setMinimumWidth(300)
    list_widget.setItemAlignment(Qt.AlignBottom)
    downBox.addWidget(list_widget)


    layout.addLayout(upBox)
    layout.addLayout(downBox)



    def start_listening():
        global stop_listening
        global voskThread
        # старт прослушивания при нажатии на кнопку
        if btn_launch_program.text() == 'Start':
            btn_launch_program.setText('Stop')
            shadow = QGraphicsDropShadowEffect(blurRadius=100, xOffset=0, yOffset=0)
            shadow.setColor(QColor(48, 213, 200))
            btn_launch_program.setGraphicsEffect(shadow)
            list_widget.clear()
            if recognizerType == "Google":
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source)
                stop_listening = recognizer.listen_in_background(microphone, handle_audio, phrase_time_limit_hotword)
            elif recognizerType == "Vosk":
                voskThread = True
                threading.Thread(target=background_listen_vosk, args=(voskThread,), daemon=True).start()
                print("Paramentr:",voskThread)


        # остановка прослушивания
        else:
            btn_launch_program.setText('Start')
            if recognizerType == "Google":
                stop_listening()
            elif recognizerType == "Vosk":
                #background_listen_vosk(False)
                voskThread = False
                print(voskThread)
            btn_launch_program.setGraphicsEffect(None)            

    def handle_audio(recognizer, audio):
        try:

            recognized_text = recognizer.recognize_google(audio, language = "ru-RU").lower()
            print(recognized_text)
            item = QListWidgetItem(recognized_text)
            list_widget.addItem(item)
            list_widget.setCurrentItem(item)
            list_widget.scrollToItem(item)
            #handle(recognized_text)
            
            if hot_word in recognized_text:
                playsound("resources\listen.wav")
                if commandrecognizerType == "Google":
                    handle_command_google()
                elif commandrecognizerType == "Vosk":
                    handle_command_vosk()
            


        except sr.UnknownValueError:
            print('Could not understand audio')
        except sr.RequestError as e:
            print('Error: ' + str(e))


    def handle_command_google():
        try:
            with mic as source:
                #recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source,10,phrase_time_limit_command)
            recognized_text = recognizer.recognize_google(audio, language = "ru-RU").lower()
            item = QListWidgetItem(recognized_text)
            list_widget.addItem(item)
            list_widget.setCurrentItem(item)
            list_widget.scrollToItem(item)
            handle(recognized_text)

            item = QListWidgetItem(recognized_text)


        except sr.UnknownValueError:
            print('Could not understand command')
        except sr.RequestError as e:
            print('Error: ' + str(e))

    def handle_command_vosk():

        # Инициализация PyAudio
        audio = pyaudio.PyAudio()
        # Параметры аудиозахвата
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=8000)
                            
        print("Говорите...")
        # Запись и распознавание речи
        while True:
            data = stream.read(16000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result['text']
                print("Распознанная речь: ", text)
                if text!= '':
                    handle(text)
                    item = QListWidgetItem(text)
                    list_widget.addItem(item)
                    list_widget.setCurrentItem(item)
                    list_widget.scrollToItem(item)
                    break
        stream.stop_stream()
        stream.close()
        audio.terminate()
            
    def background_listen_vosk(voskThread):
        # Загрузка модели распознавания речи
        print("parametr in func")
        print(voskThread)
        loop = QEventLoop()
        QTimer.singleShot(200, loop.quit)
        loop.exec_()
        model_path = "model_small"  # Укажите путь к модели Vosk
        model = vosk.Model(model_path)

        # Создание объекта распознавания
        rec = vosk.KaldiRecognizer(model, 16000)

        # Инициализация PyAudio
        audio = pyaudio.PyAudio()

        # Параметры аудиозахвата
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=8000)
                            
        print("Говорите...")

        # Запись и распознавание речи
        while voskThread == True:
            data = stream.read(16000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result['text']
                print("Распознанная речь: ", text)
                if hot_word in text:
                    print("YES")
                    playsound("resources\listen.wav")

                    if commandrecognizerType == "Google":
                        handle_command_google()
                    elif commandrecognizerType == "Vosk":
                        handle_command_vosk()
                item = QListWidgetItem(text)
                list_widget.addItem(item)
                list_widget.setCurrentItem(item)
                list_widget.scrollToItem(item)
                    
            if btn_launch_program.text() == 'Start':
                print("ITS FAAAALse")
                break
            

        # Получение финального результата
        '''''
        result = json.loads(rec.FinalResult())
        text = result['text']
        print("Финальный результат: ", text)
        '''
        # Закрытие аудиозахвата
        stream.stop_stream()
        stream.close()
        audio.terminate()

        


    start_listening()
    shortcut = QShortcut(QKeySequence("Alt+Q"), btn_launch_program)
    shortcut.activated.connect(start_listening)
    #listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    #listener_thread.start()
    btn_launch_program.clicked.connect(start_listening)
    keyboard.add_hotkey('alt+q', start_listening)


    return widget
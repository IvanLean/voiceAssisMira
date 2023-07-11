import os
import keyboard
from getWether import weather
import webbrowser as wb
import datetime
import openai
import random
import pyautogui
from gtts import gTTS
from playsound import playsound 
import os
import wikipediaapi
from PyQt5.QtCore import *
import speech_recognition as sr
from googletrans import Translator

acceptCommand = ["Готово!","Сделано!","Выполнила!","Есть!", "Окей!", "Принято!","Хорошо!"]
helloAsk=["Здравствуй!","Привет!","Приветик!","Салют!", "Здрасте!"]

recognizer = sr.Recognizer()
mic = sr.Microphone()
translator = Translator()
# Проговаривание текста
def say_text(text):
    tts = gTTS(text, lang = "ru",slow=False)
    tts.save("test.mp3")
    playsound("test.mp3") 
    os.remove("test.mp3")

def handle_text():
    try:
        say_text("Готова писать текст")
        while True:
            with mic as source:
                #recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            recognized_text = recognizer.recognize_google(audio, language = "ru-RU")
            print(recognized_text)
            keyboard.write(recognized_text + ' ')
            if(recognized_text.lower() == 'конец'):
                say_text("Закончила писать текст")
                break



    except sr.UnknownValueError:
        print('Could not understand command')
    except sr.RequestError as e:
        print('Error: ' + str(e))
# Запуск приложения или игры
def startGame(pathToExe):
    os.startfile(pathToExe)# запуск игры
# Поиск по запросу в браузере
def writeText (task):
    taskNew = task.replace('напиши', '').strip()
    keyboard.write(taskNew)

def writeFullText():
    handle_text()


def writeInEng(task):
    taskNew = task.replace('напиши на английском', '').strip()
    enTask = translator.translate(taskNew,dest='en')
    keyboard.write(enTask.text)



# Поиск в браузере
def findInBrow (task):
    taskNew = task.replace('найди в интернете', '').strip()
    print(taskNew)
    wb.open("https://yandex.ru/yandsearch?clid2028026&text={}&lr=11373".format(taskNew))
# Поиск на компьютере
def findInPC(task):

    taskNew=task.replace('найди на компьютере', '').strip()
    print(taskNew)
    keyboard.send('win+s')
    loop = QEventLoop()
    QTimer.singleShot(200, loop.quit)
    loop.exec_()

    # Вводим текст поискаПоиск
    keyboard.write(taskNew)

    # Нажимаем кнопку "Enter"
    keyboard.press_and_release('enter')
# Поиск и открытие на компьютере
def findInPCAndOpen(task):
    taskNew=task.replace('найди и открой', '').strip()
    print(taskNew)
    keyboard.send('win+s')
    loop = QEventLoop()
    QTimer.singleShot(200, loop.quit)
    loop.exec_()

    # Вводим текст поискаПоиск
    keyboard.write(taskNew)
    loop = QEventLoop()
    QTimer.singleShot(200, loop.quit)
    loop.exec_()
    # Нажимаем кнопку "Enter"
    keyboard.send('enter')
# Скриншот
def prtsc():
    pyautogui.press('prtsc')
# Получение времени
def getTime():
    time_checker = datetime.datetime.now() # Получаем текущее время с помощью datetime
    say_text('{h} {m}'.format(h=time_checker.hour, m=time_checker.minute))
# Громкость выше
def volumeUp():
    for i in range(5):
        keyboard.send("volume up")
# Громкость ниже
def volumeDown():
    for i in range(5):
        keyboard.send("volume down")
# Вкл/выкл ключевого слова
def turnHotWord(hotWordState, value):
    hotWordState = value
    if value:
        say_text("Ключевое слово активно")
        
    else:
        say_text("Ключевое слово отключено")
    print("State is", value)

    return hotWordState
# Генерация запроса и его параметры к чат ГПТ
def generate_response(prompt):# генерация запроса к гпт
    openai.api_key = ''
    response = openai.Completion.create(
        engine='text-davinci-003',  # Выберите подходящий движок
        prompt=prompt,
        max_tokens=3000,  # Максимальное количество токенов в ответе
        temperature=0.7,  # Настройте температуру генерации (чем выше значение, тем случайнее ответ)
        n=1,  # Генерируем только один ответ
        stop=None,  # Не указываем стоп-фразу для прерывания генерации
        timeout=10,  # Ограничение времени на генерацию (в секундах)
        
    )
    print("imhere")
    if response and response.choices:
        return response.choices[0].text.strip()
    return ""
# Запрос к ГПТ
def requestToGpt(text):
    prompt = text.replace('скажи', '').strip()
    say_text("Хорошо, дайте мне немного подумать")
    print(prompt)
    response = generate_response(prompt)
    say_text(response)


def get_wikipedia_definition(term, num_paragraphs):
    wiki_wiki = wikipediaapi.Wikipedia('ru')
    page_py = wiki_wiki.page(term)
    
    if page_py.exists():
        paragraphs = page_py.text.split("\n")  # Разделение текста на абзацы
        
        if num_paragraphs > len(paragraphs):
            num_paragraphs = len(paragraphs)
        
        definition = "\n".join(paragraphs[:num_paragraphs])
        return definition
    else:
        return "Страница не найдена."
def requestToWikipedia(text):
    term = text.replace('что такое', '').strip()
    num_paragraphs = 1  # Число абзацев, которые вы хотите получить
    definition = get_wikipedia_definition(term, num_paragraphs)
    print(f"Определение для '{term}' ({num_paragraphs} абзаца(ов)):")
    # Page - Summary: Python is a widely used high-level programming language for
    print(definition)
    say_text(definition)



sitesArray=[]
comsSitesArray=[]
site_dict = {
}
pathArray=[]
comsAppsArray=[]
app_dict = {
}

def handle(value):
    handlers = {
        "привет":lambda: say_text(random.choice(helloAsk)),
        "дальше":lambda: keyboard.send("next track"),
        "назад": lambda: keyboard.send("previous track"),
        "старт":lambda: keyboard.send("play/pause media"),
        "найди в интернете":lambda: findInBrow(value),
        "стоп":lambda: keyboard.send("play/pause media"),
        "громче":lambda: volumeUp(),
        "тише":lambda: volumeDown(),
        "окно":lambda: keyboard.send("alt+tab"),
        "время":lambda: getTime(),
        "погод":lambda: weather(),
        "калькулятор":lambda: os.system('calc'),
        "найди на компьютере": lambda: findInPC(value),
        "найди и открой": lambda: findInPCAndOpen(value),
        "диспетчер задач": lambda: keyboard.send("ctrl+shift+esc"),
        "рабочий стол": lambda: keyboard.send("windows+m"),
        "параметры": lambda: keyboard.send("windows+i"),
        "скриншот": lambda: prtsc(),
        "проводник": lambda: keyboard.send("windows+e"),
        "папк": lambda: keyboard.send("ctrl+shift+n"),
        "напиши на английском": lambda: writeInEng(value),
        "напиши текст": lambda: writeFullText(),
        "напиши": lambda: writeText(value),
        "принять": lambda: keyboard.send("enter"),
        "документ": lambda: os.startfile('write.exe'),
        "сохранить": lambda: keyboard.send("ctrl+s"),
        "скопировать": lambda: keyboard.send("ctrl+c"),
        "вставить": lambda: keyboard.send("ctrl+v"),
        "отменить": lambda: keyboard.send("esc"),
        "закрыть": lambda: keyboard.send("alt+f4"),
        "язык": lambda: keyboard.send("alt+shift"),
        "ниже": lambda: keyboard.send("page down"),
        "выше": lambda: keyboard.send("page up"),
        "вверх": lambda: keyboard.send("up"),
        "вниз": lambda: keyboard.send("down"),
        "влево": lambda: keyboard.send("left"),
        "вправо": lambda: keyboard.send("right"),
        "перезагрузить компьютер": lambda: os.system('shutdown /r /t 0'),
        "выключить компьютер": lambda: os.system('shutdown /s /t 0'),
        "включить вводное слово": lambda: turnHotWord(True),
        "отключить вводное слово": lambda: turnHotWord(False),
        "скажи": lambda: requestToGpt(value),
        "что такое": lambda: requestToWikipedia(value),



        

    }
    handlers = handlers | site_dict | app_dict

    command_found = False
    for command, handler in handlers.items():
        if command in value:
            handler()
            command_found = True
            if command != "привет" and command != "погод" and command != "скажи" and command != "что такое":
                say_text(random.choice(acceptCommand))
                break

    if command_found == False:
        say_text("Команды не существует")


    return "Invalid command"




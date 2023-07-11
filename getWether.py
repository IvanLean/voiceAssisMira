from playsound import playsound 
import requests
from gtts import gTTS
import json
import os
from num2words import num2words
#параметры для погоды
city = 'Volgograd'
api_key = 'ae19889495f5be6f9f28e4a7c47b3e5c'

def weather():
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api_key

        response = requests.get(url)
        data = json.loads(response.text)

        temp = int((data['main']['temp']) - 273.15)
        windSpeed = int(data['wind']['speed'])
        
        temp_str = num2words(abs(temp), lang='ru').replace('-', 'минус ')  # Преобразование числа в словесную форму
        
        text = f"Температура воздуха: {temp_str} градусов, скорость ветра: {windSpeed} метров в секунду"
        tts = gTTS(text, lang="ru")
        tts.save("test.mp3")
        playsound("test.mp3") 
        os.remove("test.mp3")

    except Exception as e:
        print("Exception (weather):", e)
        pass

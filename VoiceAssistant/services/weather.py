import requests
from geotext import GeoText
from googletrans import Translator
import json


def check_weather(text):
    city = find_city_in_string(text)
    if city is None:
        country = find_country_in_string(text)
        if country is None:
            return None
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + str(country) + '&APPID=caeadda0fd761bace210ea2cd08bf167')
        content = response.text
        return prepare_weather_string(content)
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + str(city) +'&APPID=caeadda0fd761bace210ea2cd08bf167')
    content = response.text
    return prepare_weather_string(content)


def find_city_in_string(text):
    try:
        translator = Translator()
        translate = translator.translate(text, src='pl', dest='en')
        cities = GeoText(translate.text).cities
        if len(cities) == 0:
            return None
        return cities[0]
    except Exception:
        return None


def find_country_in_string(text):
    try:
        translator = Translator()
        translate = translator.translate(text, src='pl', dest='en')
        countries = GeoText(translate.text).countries
        if len(countries) == 0:
            return None
        return countries[0]
    except Exception:
        return None


def prepare_weather_string(response):
    parsed_json = json.loads(response)
    english = "In " + parsed_json["name"] + " is " + parsed_json["weather"][0]["description"] + " and temperature is " +\
              str((parsed_json["main"]["temp"] - 275.15).__round__()) + " Celsius degrees."
    translator = Translator()
    translate = translator.translate(english, src='en', dest='pl')
    return translate.text


def get_wake_words():
    return ["pogoda"]


def wake_function(frame, text, *rest):
    weather_condition = check_weather(text)
    if weather_condition is None:
        frame.assistant_speaks("Niestety nie udało mi się znaleźć pogody dla podanego miejsca")
    else:
        frame.assistant_speaks(weather_condition)

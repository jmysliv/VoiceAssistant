import requests
import json
from googletrans import Translator
import time
from speech.speech_recognizer import get_audio


def num_to_month(num):
    with open('.././json_files/months.json', 'r') as f:
        months = json.loads(f.read())
    country = [country for country in months if country['month_number'] == num]
    return country[0]['month_name']


def get_data_about_corona(text):
    with open('.././json_files/countries.json', 'r') as f:
        countries = json.loads(f.read())
    try:
        translator = Translator()
        translate = translator.translate(text, src='pl', dest='en')
        country = [country for country in countries if country['name'] == translate.text]
        country_code = country[0]['code']
        response = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=' + str(country_code))
        if response.status_code != 200:
            return "Serwer na razie nie odpowiada, spróbuj później"
        content = json.loads(response.text)
        data = content["locations"][0]["last_updated"]
        data = data.split('-')
        year = data[0]
        month = num_to_month(data[1])
        day = data[2][:2]
        return "Dane na {} {} {} są następujące: " \
               "liczba osób zarażonych wynosi {} " \
               "liczba osób która umarła z powodu koronawirusa wynosi {} " \
               "liczba osób wyzdrowiałych wynosi {}"\
            .format(day, month, year, content["latest"]["confirmed"], content["latest"]["deaths"], content["latest"]["recovered"])

    except IndexError:
        return "Niestety nie udało się znaleźć informacji dla podanego kraju"


def get_wake_words():
    return ["koronawirus", "korona wirus"]


def wake_function(frame, *rest):
    frame.assistant_speaks("Podaj kraj dla którego chciałbyś otrzymać informacje ?")
    time.sleep(1.5)
    country_name = get_audio(5)
    while country_name == "":
        frame.assistant_doesnt_understand()
        country_name = get_audio(5)
    frame.user_speaks(country_name)
    frame.assistant_speaks(get_data_about_corona(country_name))

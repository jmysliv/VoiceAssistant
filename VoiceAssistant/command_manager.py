import speech_recognition as sr
from selenium import webdriver
import time
import jokes
import curiosities
import json_parser
import wikipedia
import weather
import event_service
import task_service

CURIO_WAKE = ["ciekawostki", "opowiedz ciekawostkę", "powiedz ciekawostkę", "powiedz coś ciekawego",
              "podaj jakąś ciekawostkę", "powiedz ciekawostkę"]

JOKES_WAKE = ["suchar", "opowiedz dowcip", "powiedz dowcip", "powiedz żart", "opowiedz kawał", "powiedz kawał",
              "opowiedz żart", "żart", "dowcip"]

ADD_EVENT_WAKE = ["dodaj wydarzenie", "dodaj nowe wydarzenie", "zaplanuj wydarzenie"]

SHOW_EVENTS_WAKE = ["pokaż wydarzenia", "wyświetl wydarzenia", "jakie mam wydarzenia", "co mam zaplanowane",
               "co mam w planach"]

ADD_TASK_WAKE = ["dodaj zadanie", "zaplanuj zadanie", "dodaj rzecz do zrobienia"]

SHOW_UNDONE_TASKS_WAKE = ["pokaż zadania do wykonania", "pokaż niezrobione zadania", "pokaż co mam do zrobienia",
                          "co mam zrobić", "co jest do zrobienia"]

SHOW_DONE_TASKS_WAKE = ["pokaż co zrobiłem", "pokaż zrobione zadania", "co zrobiłem", "co już zrobiłem"]

MARK_TASK_AS_DONE_WAKE = ["dodaj zadanie do zrobionych", "oznacz zadanie jako zrobione", "przenieś zadanie do zrobionych",
                          "zrobiłem zadanie", "wykonałem zadanie"]

YT_WAKE = ["Uruchom", "uruchom", "Włącz", "włącz", "wlacz"]

def get_audio(sample_rate, chunk_size, timeout):
    r = sr.Recognizer()
    with sr.Microphone(device_index=0, sample_rate=sample_rate, chunk_size=chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=timeout)
            text = r.recognize_google(audio, language="pl-PL")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.WaitTimeoutError as e:
            print(e)
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service;{0}".format(e))
            return ""


def start_listening(frame, token):
    wake = "Grażyna"
    sample_rate = 48000
    chunk_size = 2048
    # mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
    # mic_list = sr.Microphone.list_microphone_names()
    #
    # for i, microphone_name in enumerate(mic_list):
    #     if microphone_name == mic_name:
    #         device_id = i

    while True:
        print("Listening")
        text = get_audio(sample_rate, chunk_size, 2)

        if text.count(wake) > 0:
            frame.assistant_listening()
            text = get_audio(sample_rate, chunk_size, 5)
            while text == "":
                frame.assistant_doesnt_understand()
                text = get_audio(sample_rate, chunk_size, 5)
            frame.user_speaks(text)
            text = text.lower()
            try:
                if text in JOKES_WAKE:
                    if len(jokes.jokes) == 0:
                        frame.assistant_speaks("Chwileczkę...")
                    joke = jokes.get_random_joke()
                    frame.assistant_speaks(joke['first_part'])
                    time.sleep(5)
                    frame.assistant_speaks(joke['second_part'])
                elif text in CURIO_WAKE:
                    frame.assistant_speaks(curiosities.get_random_curio()['curio'])
                elif "uruchom" in text :
                    driver = webdriver.Chrome(executable_path=r".././drivers/chromedriver80.1.exe")
                    driver.maximize_window()
                    driver.get("https://www.youtube.com/?hl=pl&gl=PL")
                    json_parser.parse_json(".././json_files/yt.json", driver, text.replace('uruchom', '').upper())
                elif "pogoda" in text:
                    weather_condition = weather.check_weather(text)
                    if weather_condition is None:
                        frame.assistant_speaks("Niestety nie udało mi się znaleźć pogody dla podanego miejsca")
                    else:
                        frame.assistant_speaks(weather_condition)
                elif text in ADD_EVENT_WAKE:
                    frame.assistant_speaks("Podaj nazwę wydarzenia")
                    name = get_audio(sample_rate, chunk_size, 5)
                    while name == "":
                        frame.assistant_doesnt_understand()
                        name = get_audio(sample_rate, chunk_size, 5)
                    frame.user_speaks(name)
                    frame.assistant_speaks("Podaj date(w formacie: dzień miesiąc rok czas)")
                    date = get_audio(sample_rate, chunk_size, 5)
                    while date == "":
                        frame.assistant_doesnt_understand()
                        date = get_audio(sample_rate, chunk_size, 5)
                    frame.user_speaks(date)
                    frame.assistant_speaks(event_service.add_event(name, date, token))
                elif text in SHOW_EVENTS_WAKE:
                    frame.assistant_speaks(event_service.show_events(token))
                elif text in ADD_TASK_WAKE:
                    frame.assistant_speaks("Podaj nazwę zadania")
                    name = get_audio(sample_rate, chunk_size, 5)
                    while name == "":
                        frame.assistant_doesnt_understand()
                        name = get_audio(sample_rate, chunk_size, 5)
                    frame.user_speaks(name)
                    frame.assistant_speaks("Podaj date(w formacie: dzień miesiąc rok czas)")
                    date = get_audio(sample_rate, chunk_size, 5)
                    while date == "":
                        frame.assistant_doesnt_understand()
                        date = get_audio(sample_rate, chunk_size, 5)
                    frame.user_speaks(date)
                    frame.assistant_speaks(task_service.add_task(name, date, token))
                elif text in SHOW_UNDONE_TASKS_WAKE:
                    frame.assistant_speaks(task_service.show_undone_tasks(token))
                elif text in SHOW_DONE_TASKS_WAKE:
                    frame.assistant_speaks(task_service.show_finished_tasks(token))
                elif text in MARK_TASK_AS_DONE_WAKE:
                    frame.assistant_speaks("Zadanie o jakim numerze zrobiłeś?")
                    task_id = get_audio(sample_rate, chunk_size, 5)
                    while task_id == "":
                        frame.assistant_doesnt_understand()
                        task_id = get_audio(sample_rate, chunk_size, 5)
                    frame.assistant_speaks(task_service.mark_task_as_done(token, int(task_id)))
                elif "stop" in text:
                    break
                else:
                    result = wikipedia.search_in_wikipedia(text)
                    if result is not None:
                        frame.assistant_speaks(result)
            except Exception as e:
                print(e)
                pass



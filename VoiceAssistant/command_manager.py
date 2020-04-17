from speech_recognizer import get_audio
from selenium import webdriver
import time
from UI.main import isLinux
from services import coronavirus as corona, curiosities, event_service, jokes, json_parser, message_service, system_control,\
    task_service, weather, wikipedia
import winsound
import service
if not isLinux:
    import winsound
else:
    import os
    import alsaaudio


CURIO = ["ciekawostki", "ciekawego", "ciekawostki", "ciekawostka", "ciekawostkę"]

JOKES = ["suchar", "suchar", "żart", "dowcip"]

ADD_EVENT = ["dodaj wydarzenie", "dodaj nowe wydarzenie", "zaplanuj wydarzenie"]

SHOW_EVENTS = ["pokaż wydarzenia", "wyświetl wydarzenia", "jakie mam wydarzenia", "co mam zaplanowane",
               "co mam w planach"]

ADD_TASK = ["dodaj zadanie", "zaplanuj zadanie", "dodaj rzecz do zrobienia"]

SHOW_UNDONE_TASKS = ["pokaż zadania do wykonania", "pokaż niezrobione zadania", "pokaż co mam do zrobienia",
                          "co mam zrobić", "co jest do zrobienia"]

SHOW_DONE_TASKS = ["pokaż co zrobiłem", "pokaż zrobione zadania", "co zrobiłem", "co już zrobiłem"]

MARK_TASK_AS_DONE = ["dodaj zadanie do zrobionych", "oznacz zadanie jako zrobione", "przenieś zadanie do zrobionych",
                          "zrobiłem zadanie", "wykonałem zadanie"]

YT = ["uruchom", "włącz", "puść"]

CORONA = ["koronawirus", "koronawirusie", "korona wirusie", "korona wirus", "koronawirusa"]

SEND_MESSAGE = ["wyślij wiadomość", "napisz wiadomość"]

SHOW_MESSAGES = ["pokaż wysłane wiadomości", "pokaż wiadomości które wysłałem"]

SHOW_INBOX_UNREAD = ["pokaż skrzynkę odbiorczą", "mam jakieś nowę wiadomości", "pokaż nowe wiadomości"]

SHOW_INBOX_READ = ["pokaż przeczytane wiadomości", "pokaż stare wiadomości"]

MARK_MESSAGE_AS_READ = ["oznacz wiadomość jako przeczytaną", "przeczytałem wiadomość"]

VOLUME_WAKE = ["głośność", "przycisz", "podgłośni", "dźwięk"]

BRIGHTNESS_WAKE = ["jasność", "kontrast"]




def should_wake(wake_arr, text):
    for wake in wake_arr:
        if wake in text:
            return True
    return False


def start_listening(frame, token):
    wake = "Janusz"
    # mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
    # mic_list = sr.Microphone.list_microphone_names()
    #
    # for i, microphone_name in enumerate(mic_list):
    #     if microphone_name == mic_name:
    #         device_id = i

    while True:
        print("Listening")
        text = get_audio(2)
        services = service.create_services()

        if text.count(wake) > 0:
            frame.assistant_listening()
            text = get_audio(5)
            while text == "":
                frame.assistant_doesnt_understand()
                text = get_audio(5)
            frame.user_speaks(text)
            old_text = text
            text = text.lower()
            try:
                if 1:
                    for s in services:
                        if should_wake(s.wake_words, text):
                            s.wake_function(frame, text)
                # if should_wake(JOKES, text):
                #     if len(jokes.jokes) == 0:
                #         frame.assistant_speaks("Chwileczkę...")
                #     joke = jokes.get_random_joke()
                #     frame.assistant_speaks(joke['first_part'])
                #     time.sleep(5)
                #     frame.assistant_speaks(joke['second_part'])
                #     time.sleep(1)
                #     if isLinux:
                #         os.system(f'aplay .././sounds/joke.wav')
                #     else:
                #         winsound.PlaySound('.././sounds/joke.wav', winsound.SND_FILENAME)
                # elif should_wake(CURIO, text):
                #     frame.assistant_speaks(curiosities.get_random_curio()['curio'])
                # elif should_wake(VOLUME_WAKE, text):
                #     frame.assistant_speaks("Na ile mam ustawić głośności?")
                #     time.sleep(1.5)
                #     voulme = get_audio(5)
                #     while voulme == "":
                #         frame.assistant_doesnt_understand()
                #         voulme = get_audio(5)
                #     frame.user_speaks(voulme)
                #     if isLinux:
                #         m = alsaaudio.Mixer()
                #         m.setvolume(int(voulme))
                #     else:
                #         system_control_win.set_volume(int(voulme))
                #     frame.assistant_speaks("Zrobione")
                elif should_wake(BRIGHTNESS_WAKE, text):
                    frame.assistant_speaks("Na ile mam ustawić kontrast?")
                    time.sleep(1.5)
                    brightness = get_audio(5)
                    while brightness == "":
                        frame.assistant_doesnt_understand()
                        brightness = get_audio(5)
                    frame.user_speaks(brightness)
                    if isLinux:
                        connected_displays = os.popen('xrandr | grep " connected" | cut -f1 -d " "').read()
                        os.system("xrandr --output {} --brightness {}".format(connected_displays.splitlines()[0],float(brightness / 100)))
                    else:
                        system_control.set_brightness(int(brightness))
                    frame.assistant_speaks("Zrobione")
                elif should_wake(YT, text):
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
                elif should_wake(CORONA, text):
                    frame.assistant_speaks("Podaj kraj dla którego chciałbyś otrzymać informacje ?")
                    time.sleep(1.5)
                    country_name = get_audio(5)
                    while country_name == "":
                        frame.assistant_doesnt_understand()
                        country_name = get_audio(5)
                    frame.user_speaks(country_name)
                    frame.assistant_speaks(corona.get_data_about_corona(country_name))
                elif should_wake(ADD_EVENT, text):
                    frame.assistant_speaks("Podaj nazwę wydarzenia")
                    name = get_audio(5)
                    while name == "":
                        frame.assistant_doesnt_understand()
                        name = get_audio(5)
                    frame.user_speaks(name)
                    frame.assistant_speaks("Podaj date(w formacie: dzień miesiąc rok czas)")
                    date = get_audio(5)
                    while date == "":
                        frame.assistant_doesnt_understand()
                        date = get_audio(5)
                    frame.user_speaks(date)
                    frame.assistant_speaks(event_service.add_event(name, date, token))
                elif should_wake(SHOW_EVENTS, text):
                    frame.assistant_speaks(event_service.show_events(token))
                elif should_wake(ADD_TASK, text):
                    frame.assistant_speaks("Podaj nazwę zadania")
                    name = get_audio(5)
                    while name == "":
                        frame.assistant_doesnt_understand()
                        name = get_audio(5)
                    frame.user_speaks(name)
                    frame.assistant_speaks("Podaj date(w formacie: dzień miesiąc rok czas)")
                    date = get_audio(5)
                    while date == "":
                        frame.assistant_doesnt_understand()
                        date = get_audio(5)
                    frame.user_speaks(date)
                    frame.assistant_speaks(task_service.add_task(name, date, token))
                elif should_wake(SHOW_UNDONE_TASKS, text):
                    frame.assistant_speaks(task_service.show_undone_tasks(token))
                elif should_wake(SHOW_DONE_TASKS, text):
                    frame.assistant_speaks(task_service.show_finished_tasks(token))
                elif should_wake(MARK_TASK_AS_DONE, text):
                    frame.assistant_speaks("Zadanie o jakim numerze zrobiłeś?")
                    task_id = get_audio(5)
                    while task_id == "":
                        frame.assistant_doesnt_understand()
                        task_id = get_audio(5)
                    frame.assistant_speaks(task_service.mark_task_as_done(token, int(task_id)))
                elif should_wake(SEND_MESSAGE, text):
                    frame.assistant_speaks("Do kogo chcesz wysłać wiadomość")
                    receiver = get_audio(5)
                    while receiver == "":
                        frame.assistant_doesnt_understand()
                        receiver = get_audio(5)
                    frame.user_speaks(receiver)
                    frame.assistant_speaks("Podaj wiadomość: ")
                    content = get_audio(5)
                    while content == "":
                        frame.assistant_doesnt_understand()
                        content = get_audio(5)
                    frame.user_speaks(content)
                    frame.assistant_speaks(message_service.send_message(receiver, content, token))
                elif should_wake(SHOW_MESSAGES, text):
                    frame.assistant_speaks(message_service.show_sent_messages(token))
                elif should_wake(SHOW_INBOX_READ, text):
                    frame.assistant_speaks(message_service.show_read_messages(token))
                elif should_wake(SHOW_INBOX_UNREAD, text):
                    frame.assistant_speaks(message_service.show_unread_messages(token))
                elif should_wake(MARK_MESSAGE_AS_READ, text):
                    frame.assistant_speaks("Wiadomość o jakim numerzę przeczytałeś?")
                    message_id = get_audio(5)
                    while message_id == "":
                        frame.assistant_doesnt_understand()
                        message_id = get_audio(5)
                    frame.assistant_speaks(message_service.mark_message_as_read(token, int(message_id)))
                elif "stop" in text:
                    break
                else:
                    frame.assistant_speaks(wikipedia.search_in_wikipedia(old_text))
            except Exception as e:
                print(e)
                pass



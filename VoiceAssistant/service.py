from services import jokes, curiosities, system_control, json_parser, weather, coronavirus, event_service, task_service, \
    message_service, wikipedia


class Service:
    def __init__(self, wake_words, wake_function):
        self.wake_words = wake_words
        self.wake_function = wake_function  # should take 2 arguments [frame, text]


def stop(frame, *rest):
    frame.assistant_speaks("Miło, że mogłem pomóc. Do zobaczenia!")

def create_services():
    services = list()
    services.append(Service(["suchar", "suchar", "żart", "dowcip"], jokes.wake_function))
    services.append(Service(["ciekawostki", "ciekawego", "ciekawostki", "ciekawostka", "ciekawostkę"],
                            curiosities.wake_function))
    services.append(Service(["głośność", "przycisz", "podgłośni", "dźwięk"], system_control.volume_wake_function))
    services.append(Service(["jasność", "kontrast"], system_control.brightness_wake_function))
    services.append(Service(["uruchom", "włącz", "puść"], json_parser.youtube_wake_function))
    services.append(Service(["pogoda"], weather.weather_wake_function))
    services.append(Service(["koronawirus", "koronawirusie", "korona wirusie", "korona wirus", "koronawirusa"],
                            coronavirus.coronavirus_wake_function))
    services.append(Service(["dodaj wydarzenie", "dodaj nowe wydarzenie", "zaplanuj wydarzenie"],
                            event_service.add_event_wake_function))
    services.append(Service(["pokaż wydarzenia", "wyświetl wydarzenia", "jakie mam wydarzenia", "co mam zaplanowane",
                             "co mam w planach"], event_service.show_events_wake_functions))
    services.append(Service(["dodaj zadanie", "zaplanuj zadanie", "dodaj rzecz do zrobienia"],
                            task_service.add_task_wake_function))
    services.append(Service(["pokaż zadania do wykonania", "pokaż niezrobione zadania", "pokaż co mam do zrobienia",
                             "co mam zrobić", "co jest do zrobienia"], task_service.show_undone_task_wake_function))
    services.append(Service(["pokaż co zrobiłem", "pokaż zrobione zadania", "co zrobiłem", "co już zrobiłem"],
                            task_service.show_done_task_wake_function))
    services.append(Service(["dodaj zadanie do zrobionych", "oznacz zadanie jako zrobione",
                             "przenieś zadanie do zrobionych", "zrobiłem zadanie", "wykonałem zadanie"],
                            task_service.mark_task_wake_function))
    services.append(Service(["wyślij wiadomość", "napisz wiadomość"], message_service.send_message_wake_function))
    services.append(Service(["pokaż wysłane wiadomości", "pokaż wiadomości które wysłałem"],
                            message_service.show_messages_wake_function))
    services.append(Service(["pokaż przeczytane wiadomości", "pokaż stare wiadomości"],
                            message_service.show_inbox_read_wake_function))
    services.append(Service(["pokaż skrzynkę odbiorczą", "mam jakieś nowę wiadomości", "pokaż nowe wiadomości"],
                            message_service.show_inbox_wake_function))
    services.append(Service(["oznacz wiadomość jako przeczytaną", "przeczytałem wiadomość"],
                            message_service.mark_message_wake_function))
    services.append(Service(["stop", "zakończ", "narazie asysteńcie", "do widzenia asysteńcie"], stop))

    last_service = Service([], wikipedia.wikipedia_wake_function)
    return services, last_service

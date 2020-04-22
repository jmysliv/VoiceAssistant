from speech.speech_recognizer import get_audio
from services.task_service import add_task


def get_wake_words():
    return ["dodaj zadanie", "zaplanuj zadanie", "dodaj rzecz do zrobienia"]


def wake_function(frame, text, token):
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
    frame.assistant_speaks(add_task(name, date, token))

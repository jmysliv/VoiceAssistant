from speech.speech_recognizer import get_audio
from services.task_service import mark_task_as_done


def get_wake_words():
    return ["dodaj zadanie do zrobionych", "oznacz zadanie jako zrobione",
            "przenieś zadanie do zrobionych", "zrobiłem zadanie", "wykonałem zadanie"]


def wake_function(frame, text, token):
    frame.assistant_speaks("Zadanie o jakim numerze zrobiłeś?")
    task_id = get_audio(5)
    while task_id == "":
        frame.assistant_doesnt_understand()
        task_id = get_audio(5)
    frame.assistant_speaks(mark_task_as_done(token, int(task_id)))

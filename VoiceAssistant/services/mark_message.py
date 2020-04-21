from speech.speech_recognizer import get_audio
from services.message_service import mark_message_as_read


def get_wake_words():
    return ["oznacz wiadomość jako przeczytaną", "przeczytałem wiadomość"]


def wake_function(frame, text, token):
    frame.assistant_speaks("Wiadomość o jakim numerzę przeczytałeś?")
    message_id = get_audio(5)
    while message_id == "":
        frame.assistant_doesnt_understand()
        message_id = get_audio(5)
    frame.assistant_speaks(mark_message_as_read(token, int(message_id)))

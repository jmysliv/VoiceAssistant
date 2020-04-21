from speech.speech_recognizer import get_audio
from services.message_service import send_message


def get_wake_words():
    return ["wyślij wiadomość", "napisz wiadomość"]


def wake_function(frame, text, token):
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
    frame.assistant_speaks(send_message(receiver, content, token))

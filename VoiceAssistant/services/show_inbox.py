from services.message_service import show_unread_messages


def get_wake_words():
    return ["pokaż skrzynkę odbiorczą", "mam jakieś nowę wiadomości", "pokaż nowe wiadomości"]


def wake_function(frame, text, token):
    frame.assistant_speaks(show_unread_messages(token))

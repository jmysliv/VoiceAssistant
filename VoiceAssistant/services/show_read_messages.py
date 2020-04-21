from services.message_service import show_read_messages


def get_wake_words():
    return ["pokaż przeczytane wiadomości", "pokaż stare wiadomości"]


def wake_function(frame, text, token):
    frame.assistant_speaks(show_read_messages(token))

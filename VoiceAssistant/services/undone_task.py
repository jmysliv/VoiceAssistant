from services.task_service import show_undone_tasks


def get_wake_words():
    return ["zadania do wykonania", "niezrobione zadania", "co mam zrobić", "co jest do zrobienia"]


def wake_function(frame, text, token):
    frame.assistant_speaks(show_undone_tasks(token))

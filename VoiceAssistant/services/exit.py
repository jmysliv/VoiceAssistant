import time


def get_wake_words():
    return ["stop", "zakończ", "na razie asystencie", "do widzenia asystencie"]


def wake_function(frame, *rest):
    frame.assistant_speaks("Miło, że mogłem pomóc. Do zobaczenia!")
    time.sleep(3)
    frame.quit()
    exit()

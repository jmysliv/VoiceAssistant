from speech.speech_recognizer import get_audio
import service
import time
from UI.main import stemmer


def should_wake(wake_arr, text):
    text_array = text.split(" ")
    stemmed_text = ""
    for word in text_array:
        stemmed_text = stemmed_text + " " + stemmer.stem(word)
    for wake in wake_arr:
        stemmed_wake = ""
        for word in wake.split(" "):
            stemmed_wake = stemmed_wake + " " + stemmer.stem(word)
        if stemmed_wake in stemmed_text:
            return True
    return False


def start_listening(frame, token):
    wake = "Janusz"
    try:
        services, last_service = service.create_services()
    except AttributeError:
        time.sleep(3)
        frame.assistant_speaks("Jeden z dodanych serwisów, nie ma zdefiniowanych wymaganych funkcji. "
                             "Aby korzystać z asystenta napraw ten błąd.")
        time.sleep(11)
        frame.quit()
        return
    except ValueError as e:
        time.sleep(3)
        frame.assistant_speaks(str(e))
        time.sleep(11)
        frame.quit()
        return

    while True:
        text = get_audio(2)
        
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
                for index, s in enumerate(services):
                    if should_wake(s.wake_words, text):
                        s.wake_function(frame, text, token)
                        break
                    if index + 1 == len(services) and last_service is not None:
                        last_service.wake_function(frame, old_text, token)

            except Exception as e:
                print(e)
                pass



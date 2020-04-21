from speech.speech_recognizer import get_audio
import service


def should_wake(wake_arr, text):
    for wake in wake_arr:
        if wake in text:
            return True
    return False


def start_listening(frame, token):
    wake = "Janusz"
    services, last_service = service.create_services()

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



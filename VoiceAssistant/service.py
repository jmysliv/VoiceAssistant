import glob
import importlib
import os


class Service:
    def __init__(self, wake_words, wake_function):
        self.wake_words = wake_words
        self.wake_function = wake_function  # should take 3 arguments [frame, text, token]


def check_wake_words_uniqueness(services):
    words = dict()
    for service in services:
        for wake_word in service.wake_words:
            if wake_word in words:
                print(words)
                print(wake_word)
                return False
            else:
                words[wake_word] = 1
    return True


def create_services():
    services = list()
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    module_name = "services"
    for file in glob.glob(current_dir + "/services/*.py"):
        name = os.path.splitext(os.path.basename(file))[0]
        module = importlib.import_module("." + name, package=module_name)
        services.append(Service(module.get_wake_words(), module.wake_function))

    if not check_wake_words_uniqueness(services):
        raise ValueError("Co najmniej dwa serwisy używają tego samego 'wake word' mimo, iż powinny one być unikalne. "
                         "Napraw ten błąd by móc korzystać z asystenta")

    last_service = None
    for service in services:
        if service.wake_words == []:
            last_service = service
    if last_service is not None:
        services.remove(last_service)

    return services, last_service

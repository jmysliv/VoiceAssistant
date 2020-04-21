import glob
import importlib
import os


class Service:
    def __init__(self, wake_words, wake_function):
        self.wake_words = wake_words
        self.wake_function = wake_function  # should take 3 arguments [frame, text, token]


def create_services():
    services = list()
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    module_name = "services"
    for file in glob.glob(current_dir + "/services/*.py"):
        name = os.path.splitext(os.path.basename(file))[0]
        module = importlib.import_module("." + name, package=module_name)
        services.append(Service(module.get_wake_words(), module.wake_function))

    #check that wake_words are unique

    last_service = None
    for service in services:
        if service.wake_words == []:
            last_service = service
    if last_service is not None:
        services.remove(last_service)

    return services, last_service

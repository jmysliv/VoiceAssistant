from services import jokes, curiosities


class Service:
    def __init__(self, wake_words, wake_function):
        self.wake_words = wake_words
        self.wake_function = wake_function  # should take 2 arguments [frame, text]


def create_services():
    services = list()
    services.append(Service(["suchar", "suchar", "żart", "dowcip"], jokes.wake_function))
    services.append(Service(["ciekawostki", "ciekawego", "ciekawostki", "ciekawostka", "ciekawostkę"],
                            curiosities.wake_function))
    services.append(Service(["głośność", "przycisz", "podgłośni", "dźwięk"], ))
    return services

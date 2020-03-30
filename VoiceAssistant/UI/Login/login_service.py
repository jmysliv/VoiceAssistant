Users = [{"Antek", "pajac"}, {"Bomba", "debil"}]


def login(username, password):
    return {username, password} in Users


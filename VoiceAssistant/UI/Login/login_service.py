import validators
import requests

API_ENDPOINT = "http://46.101.198.229:6000/auth/"


def validate(username, password):
    if validators.length(username, 2, 20) is not True:
        return "Nazwa użytkownika powinna zawierać pomiędzy 2 a 20 znaków"
    if validators.length(password, 8, 30) is not True:
        return "Hasło musi mieć co najmniej 8 znaków"

    return "ok"


def login(username, password):
    data = {'username': username,
            'password': password}
    response = requests.post(API_ENDPOINT, data=data)

    if response.status_code == 400:
        return "Niepoprawne dane logowania", ""
    elif response.status_code == 200:
        token = response.json()['token']
        return "ok", token
    else:
        return "Nie mozna się zalogować", ""



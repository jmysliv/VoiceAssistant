import validators
import requests

API_ENDPOINT = "http://46.101.198.229:6000/register/"


def validate(username, email, password, conf_pass):
    if validators.length(username, 2, 20) is not True:
        return "Nazwa użytkownika powinna zawierać pomiędzy 2 a 20 znaków"
    if validators.email(email) is not True:
        return "Niepoprawny adres email"
    if validators.length(password, 8, 30) is not True:
        return "Hasło musi mieć co najmniej 8 znaków"
    if password != conf_pass:
        return "Hasła nie są identyczne"

    return "ok"


def register(username, email, password):
    data = {'username': username,
            'email': email,
            'password': password}
    response = requests.post(API_ENDPOINT, data=data)
    if response.status_code == 400:
        return "Użytkownik o podanej nazwie istnieje"
    elif response.status_code == 201:
        return "ok"
    else:
        return "Nie mozna stworzyc użytkownika"

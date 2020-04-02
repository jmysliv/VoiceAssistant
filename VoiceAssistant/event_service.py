import requests
import datetime
import time
import locale

API_ENDPOINT = "http://46.101.198.229:6000/events/"


def parse_months_name(date):
    date = date.replace(' styczeń ', '/01/')
    date = date.replace(' stycznia ', '/01/')
    date = date.replace(' luty ', '/02/')
    date = date.replace(' lutego ', '/02/')
    date = date.replace(' marzec ', '/03/')
    date = date.replace(' marca ', '/03/')
    date = date.replace(' kwietnia ', '/04/')
    date = date.replace(' kwiecień ', '/04/')
    date = date.replace(' maj ', '/05/')
    date = date.replace(' maja ', '/05/')
    date = date.replace(' czerwiec ', '/06/')
    date = date.replace(' czerwca ', '/06/')
    date = date.replace(' lipiec ', '/07/')
    date = date.replace(' lipca ', '/07/')
    date = date.replace(' sierpień ', '/08/')
    date = date.replace(' sierpnia ', '/08/')
    date = date.replace(' wrzesień ', '/09/')
    date = date.replace(' wrzesnia ', '/09/')
    date = date.replace(' październik ', '/10/')
    date = date.replace(' października ', '/10/')
    date = date.replace(' listopad ', '/11/')
    date = date.replace(' listopada ', '/11/')
    date = date.replace(' grudzień ', '/12/')
    date = date.replace(' grudnia ', '/12/')
    return date


def parse_events_list(response):
    events_string = ""
    for event in response:
        date = datetime.datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%SZ')
        if  date > datetime.datetime.now():
            events_string = events_string + str(event['id']) + ". " + event['event_name'] + " zaplanowane na " + \
                            datetime.datetime.strftime(date, '%d/%m/%Y %H:%M') + "\n"
    return events_string


def add_event(name, date_string, token):
    try:
        date = datetime.datetime.strptime(parse_months_name(date_string), '%d/%m/%Y %H:%M')
    except:
        return "Podana data jest nieprawidłowa"

    data = {'event_name': name,
            'date': date}
    headers = {'Authorization': 'Token ' + token}
    response = requests.post(API_ENDPOINT, data=data, headers=headers)
    if response.status_code == 201:
        return "Dodano wydarzenie"
    else:
        return "Nie udało się dodać wydarzenia"


def show_events(token):
    headers = {'Authorization': 'Token ' + token}
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return parse_events_list(response.json())
    else:
        return "Nie udało się pobrać wydarzeń"

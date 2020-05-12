import requests
import datetime

API_ENDPOINT = "http://46.101.198.229:6000/messages/"
API_ENDPOINT_INBOX = "http://46.101.198.229:6000/inbox/"


def parse_sent_messages_list(response):
    messages_string = ""
    for message in response:
        date = datetime.datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if message['is_read']:
            read = " przeczytał "
        else:
            read = " nie przeczytał "
        messages_string = messages_string + str(message['id']) + ". " + message['receiver'] + read + \
                          "wiadomości od Ciebie wysłanej mu " + datetime.datetime.strftime(date, '%d/%m/%Y %H:%M') +\
                            " o treści: " + message['content'] + "\n"
    return messages_string


def parse_inbox_messages(response, read):
    messages_string = ""
    for message in response:
        if message['is_read'] == read:
            date = datetime.datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            messages_string = messages_string + str(message['id']) + ". " + message['sender'] +\
                          " wysłał Ci wiadomość " + datetime.datetime.strftime(date, '%d/%m/%Y %H:%M') + \
                          " o treści: " + message['content'] + "\n"
    return messages_string


def send_message(receiver, content, token):
    data = {'receiver': receiver,
            'content': content,
            'date': datetime.datetime.now()}
    headers = {'Authorization': 'Token ' + token}
    response = requests.post(API_ENDPOINT, data=data, headers=headers)
    if response.status_code == 201:
        return "Wysłano wiadomość"
    else:
        return "Nie udało się wysłać wiadomości"


def show_sent_messages(token):
    headers = {'Authorization': 'Token ' + token}
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return parse_sent_messages_list(response.json())
    else:
        return "Nie udało się pobrać wysłanych wiadomości"


def show_unread_messages(token):
    headers = {'Authorization': 'Token ' + token}
    response = requests.get(API_ENDPOINT_INBOX, headers=headers)
    if response.status_code == 200:
        return parse_inbox_messages(response.json(), False)
    else:
        return "Nie udało się pobrać wiadomości"


def show_read_messages(token):
    headers = {'Authorization': 'Token ' + token}
    response = requests.get(API_ENDPOINT_INBOX, headers=headers)
    if response.status_code == 200:
        return parse_inbox_messages(response.json(), True)
    else:
        return "Nie udało się pobrać wiadomości"


def mark_message_as_read(token, id):
    data = {'is_read': True,
            'receiver': 'receiver',
            'content': 'content'}       # receiver and content doesnt matters, but they are required to be validated
    headers = {'Authorization': 'Token ' + token}
    response = requests.put(API_ENDPOINT + str(id) + '/', data=data, headers=headers)
    if response.status_code == 200:
        return "Oznaczono wiadomość jako przeczytaną"
    else:
        return "Nie udało się oznaczyć wiadomości o podanym numerze"


def get_wake_words():
    return ["pokaż wiadomości", "pokaż wiadomości które wysłałem"]


def wake_function(frame, text, token):
    frame.assistant_speaks(show_sent_messages(token))



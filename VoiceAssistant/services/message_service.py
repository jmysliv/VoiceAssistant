import requests
import datetime
from speech_recognizer import get_audio

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
            'content': content}
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
    data = {'is_read': True}
    headers = {'Authorization': 'Token ' + token}
    response = requests.put(API_ENDPOINT + str(id) + '/', data=data, headers=headers)
    if response.status_code == 200:
        return "Oznaczono wiadomość jako przeczytaną"
    else:
        return "Nie udało się oznaczyć wiadomości o podanym numerze"


def send_message_wake_function(frame, text, token):
    frame.assistant_speaks("Do kogo chcesz wysłać wiadomość")
    receiver = get_audio(5)
    while receiver == "":
        frame.assistant_doesnt_understand()
        receiver = get_audio(5)
    frame.user_speaks(receiver)
    frame.assistant_speaks("Podaj wiadomość: ")
    content = get_audio(5)
    while content == "":
        frame.assistant_doesnt_understand()
        content = get_audio(5)
    frame.user_speaks(content)
    frame.assistant_speaks(send_message(receiver, content, token))


def show_messages_wake_function(frame, text, token):
    frame.assistant_speaks(show_sent_messages(token))


def show_inbox_read_wake_function(frame, text, token):
    frame.assistant_speaks(show_read_messages(token))


def show_inbox_wake_function(frame, text, token):
    frame.assistant_speaks(show_unread_messages(token))


def mark_message_wake_function(frame, text, token):
    frame.assistant_speaks("Wiadomość o jakim numerzę przeczytałeś?")
    message_id = get_audio(5)
    while message_id == "":
        frame.assistant_doesnt_understand()
        message_id = get_audio(5)
    frame.assistant_speaks(mark_message_as_read(token, int(message_id)))

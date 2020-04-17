import requests
import datetime


API_ENDPOINT = "http://46.101.198.229:6000/tasks/"


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


def parse_tasks_list(response, is_done):
    tasks_string = ""
    for task in response:
        date = datetime.datetime.strptime(task['date'], '%Y-%m-%dT%H:%M:%SZ')
        if task['is_done'] == is_done:
            tasks_string = tasks_string + str(task['id']) + ". " + task['task_name'] + " trzeba zrobić do " + \
                            datetime.datetime.strftime(date, '%d/%m/%Y %H:%M') + "\n"
    return tasks_string


def add_task(name, date_string, token):
    try:
        date = datetime.datetime.strptime(parse_months_name(date_string), '%d/%m/%Y %H:%M')
    except ValueError:
        return "Podana data jest nieprawidłowa"

    data = {'task_name': name,
            'date': date}
    headers = {'Authorization': 'Token ' + token}
    response = requests.post(API_ENDPOINT, data=data, headers=headers)
    if response.status_code == 201:
        return "Dodano zadanie"
    else:
        return "Nie udało się dodać zadania"


def show_undone_tasks(token):
    headers = {'Authorization': 'Token ' + token}
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return parse_tasks_list(response.json(), False)
    else:
        return "Nie udało się pobrać zadań"


def show_finished_tasks(token):
    headers = {'Authorization': 'Token ' + token}
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return parse_tasks_list(response.json(), True)
    else:
        return "Nie udało się pobrać zadań"


def mark_task_as_done(token, id):
    headers = {'Authorization': 'Token ' + token}
    response = requests.get(API_ENDPOINT + str(id) + "/", headers=headers)
    if response.status_code != 200:
        return "Nie udało się zaktualizować zadania"

    data = {'task_name': response.json()['name'],
            'is_done': True}
    response = requests.post(API_ENDPOINT + str(id) + "/", data=data, headers=headers)
    if response.status_code == 200:
        return "Zaktualizowano zadanie"
    else:
        return "Nie udało się zaktualizować zadania"

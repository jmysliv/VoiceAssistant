from bs4 import BeautifulSoup
import requests
# from pymongo import MongoClient
#
# client = MongoClient('url_bazy')
# db = client['curiosities']


def get_curiosities():
    print('scrapping starts')
    curiosities = []
    response = requests.get('https://pl.wikipedia.org/wiki/Portal:Informatyka/Ciekawostki')
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    for c in soup.find('div', class_ = 'mw-parser-output').findAll('li'):
        try:
            t = c.text
            curio = {
                "curio": t
            }
            curiosities.append(curio)
        except Exception as e:
            print(e)
            pass
    response = requests.get('https://pl.wikipedia.org/wiki/Portal:Zoologia/Ciekawostki')
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    for c in soup.find('div', class_='mw-parser-output').findAll('li'):
        try:
            t = 'Czy wiesz, że' + c.text
            curio = {
                "curio": t
            }
            curiosities.append(curio)
        except Exception as e:
            print(e)
            pass
    response = requests.get('https://pl.wikipedia.org/wiki/Portal:%C5%BBegluga/Ciekawostki')
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    for c in soup.find('div', class_='mw-parser-output').findAll('li'):
        try:
            t = 'Czy wiesz, że' + c.text
            curio = {
                "curio": t
            }
            curiosities.append(curio)
        except Exception as e:
            print(e)
            pass
    response = requests.get('https://pl.wikipedia.org/wiki/Portal:%C5%BBeglarstwo/Czy_wiesz,_%C5%BCe')
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    for c in soup.find('div', class_='mw-parser-output').findAll('li'):
        try:
            t = c.text
            curio = {
                "curio": t
            }
            curiosities.append(curio)
        except Exception as e:
            print(e)
            pass



    for curio in curiosities:
        print(curio)
        # db.curiosities.insert_one(curio)
    print("done")
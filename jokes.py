from bs4 import BeautifulSoup
import requests
# from pymongo import MongoClient
#
# client = MongoClient('url_bazy')
# db = client['jokes']


def get_jokes():
    print('scrapping starts')
    response = requests.get('https://sucharry.pl/')
    jokes = []
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    for joke in soup.findAll('div', class_='suchar'):
        try:
            first_part = joke.find('a', class_='link').text
            second_part = joke.find('a', class_='showtxt')['data-txt']
            joke = {
                "first_part": first_part,
                "second_part": second_part
            }
            jokes.append(joke)
        except Exception as e:
            print(e)
            pass


    for joke in jokes:
        print(joke)
        # db.jokes.insert_one(joke)
    print("done")

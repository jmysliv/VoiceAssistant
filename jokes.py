from bs4 import BeautifulSoup
import requests
# from pymongo import MongoClient
#
# client = MongoClient('url_bazy')
# db = client['jokes']


def get_jokes():
    print('scrapping starts')
    jokes = []
    for page_number in range(1, 30):
        if page_number > 1:
            response = requests.get('https://sucharry.pl/strona/' + str(page_number))
        else:
            response = requests.get('https://sucharry.pl/')
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

from bs4 import BeautifulSoup
import requests
from services import json_parser
from selenium import webdriver
import re
import threading


def is_wikipedia_page_exist(search_phrase):
    search = search_phrase.replace(" ", "_")
    response = requests.get('https://pl.wikipedia.org/wiki/' + search)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    try:
        result = soup.find('div', class_="plainlinks").b.text
        if result == 'W Wikipedii nie ma jeszcze artykułu o takiej nazwie. Możesz:':
            return False
    except AttributeError:
        pass
    return True


def search_in_google(search_phrase):
    driver = webdriver.Chrome(executable_path=r".././drivers/chromedriver80.1.exe")
    driver.maximize_window()
    driver.get("https://www.google.pl/")
    json_parser.parse_json(".././json_files/google.json", driver, search_phrase)


def search_in_wikipedia(search_phrase):
    if not is_wikipedia_page_exist(search_phrase):
        threading.Thread(target=search_in_google, args=([search_phrase]), daemon=True).start()
        return "Oto wyniki wyszukiwania w google"
    else:
        response = requests.get('https://pl.wikipedia.org/wiki/' + str(search_phrase.replace(" ", "_")))
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        try:
            test = soup.find('a', href="/wiki/Wikipedia:Strona_ujednoznaczniaj%C4%85ca")
            if test is not None and test['title'] == "Ujednoznacznienie":
                new_address = soup.find('div', class_="mw-parser-output").ul.li.a['href']
                response = requests.get('https://pl.m.wikipedia.org/' + str(new_address))
                content = response.text
                soup = BeautifulSoup(content, "html.parser")
            result = soup.find('div', class_="mw-parser-output").p.text
            result = re.sub(r"\[\d\]", "", result)
            return result
        except AttributeError:
            threading.Thread(target=search_in_google, args=([search_phrase]), daemon=True).start()
            return "Oto wyniki wyszukiwania w google"
        except TypeError:
            threading.Thread(target=search_in_google, args=([search_phrase]), daemon=True).start()
            return "Oto wyniki wyszukiwania w google"


def get_wake_words():
    return []


def wake_function(frame, old_text, *rest):
    frame.assistant_speaks(search_in_wikipedia(old_text))

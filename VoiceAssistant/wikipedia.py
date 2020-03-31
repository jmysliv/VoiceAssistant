from bs4 import BeautifulSoup
import requests
import json_parser
from selenium import webdriver
import re


def is_wikipedia_page_exist(search_phrase):
    response = requests.get('https://pl.m.wikipedia.org/wiki/' + str(search_phrase))
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    try:
        result = soup.find('div', class_="plainlinks").b.text
        if result == 'W Wikipedii nie ma jeszcze artykułu o takiej nazwie. Możesz:':
            return False
    except Exception as e:
        pass
    return True


def search_in_google(search_phrase):
    driver = webdriver.Chrome(executable_path=r"./drivers/chromedriver80.exe")
    driver.maximize_window()
    driver.get("https://www.google.pl/")
    json_parser.parse_json("./json_files/google.json", driver, search_phrase)


def search_in_wikipedia(search_phrase):
    if not is_wikipedia_page_exist(search_phrase):
        print("not find")
        search_in_google(search_phrase)
        return None
    else:
        response = requests.get('https://pl.m.wikipedia.org/wiki/' + str(search_phrase))
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        try:
            test = soup.find('a', href="/wiki/Wikipedia:Strona_ujednoznaczniaj%C4%85ca")
            if test is not None:
                new_address = soup.find('div', class_="mw-parser-output").ul.li.a['href']
                response = requests.get('https://pl.m.wikipedia.org/' + str(new_address))
                content = response.text
                soup = BeautifulSoup(content, "html.parser")
            result = soup.find('div', class_="mw-parser-output").p.text
            result = re.sub(r"\[\d\]", "", result)
            return result
        except Exception as e:
            print("not find")
            search_in_google(search_phrase)
            return None

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.wait import WebDriverWait
import json


def wait_to_end(s):
    tmp = s.split(':')
    time.sleep(int(tmp[0]) * 60 + int(tmp[1]) + 1)


def parse_json(json_path, driver, search):

    with open(json_path, 'r') as f:
        commands_dict = json.loads(f.read())

    for command in commands_dict:
        time.sleep(0.5)
        try:
            element = WebDriverWait(driver, command.get("timeout"))\
                .until(EC.presence_of_element_located((getattr(By, command.get("search_by")), command.get("element_name"))))
            if command["element_name"] == "search" or command["element_name"] == "input":
                element.send_keys(search)
        except TimeoutException:
            print("Loading took too much time!")
        if command.get("args"):
            for arg in command.get("args"):
                func = getattr(element, arg)
                func()
        commands_to_run = command.get("run")
        if commands_to_run:
            for i in range(0, len(commands_to_run), 2):
                globals()[commands_to_run[i]](getattr(element, commands_to_run[i+1]))


driver = webdriver.Chrome(executable_path=r"/home/sebastian/repos/VoiceAssistant/chromedriver")
driver.maximize_window()
driver.get("https://www.google.pl/")
parse_json("/home/sebastian/PycharmProjects/voiceAssistant/google.json", driver, "despascito")

# try:
#     element = WebDriverWait(driver, 3) \
#         .until(EC.presence_of_element_located("By", command.get("element_name"))))
#     if command["element_name"] == "search" or command["element_name"] == "input":
#         element.send_keys(search)
# except TimeoutException:
#     print("Loading took too much time!")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.wait import WebDriverWait
import json
from UI.main import isLinux


def wait_to_end(s):
    tmp = s.split(':')
    # time.sleep(int(tmp[0]) * 60 + int(tmp[1]) + 1)


def parse_json(json_path, driver, search):

    with open(json_path, 'r') as f:
        commands_dict = json.loads(f.read())

    for command in commands_dict:
        time.sleep(1)
        try:
            element = WebDriverWait(driver, command.get("timeout"))\
                .until(EC.presence_of_element_located((getattr(By, command.get("search_by")), command.get("element_name"))))
            if command["send_keys"]:
                element.send_keys(search)
                element.send_keys(Keys.RETURN)
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


# driver = webdriver.Chrome(executable_path=r"./drivers/chromedriver80.1.exe")
# # driver.maximize_window()
# # driver.get("https://www.google.com/")
# # parse_json("./json_files/google.json", driver, "despascito")
# time.sleep(2)
# driver.get("https://www.youtube.com/?hl=pl&gl=PL")
# parse_json("./json_files/yt.json", driver, "despascito")


def get_wake_words():
    return ["uruchom", "włącz", "puść"]


def wake_function(frame, text, *rest):
    if isLinux:
        driver = webdriver.Chrome(executable_path=r".././drivers/chromedriver")
    else:
        driver = webdriver.Chrome(executable_path=r".././drivers/chromedriver.exe")
    driver.maximize_window()
    driver.get("https://www.youtube.com/?hl=pl&gl=PL")
    parse_json(".././json_files/yt.json", driver, text.replace('uruchom', '').upper())



import speech_recognition as sr
from selenium import webdriver
import jokes
import curiosities
import json_parser
import wikipedia


mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()
mic_list = sr.Microphone.list_microphone_names()

for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name:
        device_id = i

with sr.Microphone(device_index=0, sample_rate=sample_rate, chunk_size=chunk_size) as source:
    r.adjust_for_ambient_noise(source)
    print("Say Something")
    audio = r.listen(source, timeout=5)

    try:
        text = r.recognize_google(audio, language="pl-PL")
        print("you said: " + text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service;{0}".format(e))

if text == "suchar":
    print(jokes.get_random_joke())

if text == "ciekawostki":
    curiosities.get_curiosities()

if "Uruchom" in text:
    driver = webdriver.Chrome(executable_path=r"./drivers/chromedriver")
    driver.maximize_window()
    driver.get("https://www.youtube.com/?hl=pl&gl=PL")
    print(text.replace('uruchom', ''))
    json_parser.parse_json("./json_files/yt.json", driver, text.replace('uruchom', ''))
    print(curiosities.get_random_curio())

wikipedia.search_in_wikipedia(text)


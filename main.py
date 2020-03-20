import speech_recognition as sr
from selenium import webdriver
import jokes
import curiosities
import json_parser
import wikipedia

WAKE = "Grażyna"
mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
sample_rate = 48000
chunk_size = 2048

mic_list = sr.Microphone.list_microphone_names()

for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name:
        device_id = i

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0, sample_rate=sample_rate, chunk_size=chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=2)
            text = r.recognize_google(audio, language="pl-PL")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.WaitTimeoutError as e:
            print(e)
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service;{0}".format(e))

while True:
    print("Listening")
    text = get_audio()

    if text.count(WAKE) > 0:
        print("I am ready")
        text = get_audio()
        if text == "suchar":
            print(jokes.get_random_joke())
        elif text == "ciekawostki":
            print(curiosities.get_random_curio())
        elif "Uruchom" in text:
            driver = webdriver.Chrome(executable_path=r"./drivers/chromedriver80.exe")
            driver.maximize_window()
            driver.get("https://www.youtube.com/?hl=pl&gl=PL")
            json_parser.parse_json("./json_files/yt.json", driver, text.replace('uruchom', ''))
        else:
            result = wikipedia.search_in_wikipedia(text)
            if result is not None:
                print(result)



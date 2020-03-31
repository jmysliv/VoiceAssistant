import speech_recognition as sr
from selenium import webdriver
import time
import jokes
import curiosities
import json_parser
import wikipedia
import weather

CURIO_WAKE = ["ciekawostki", "opowiedz ciekawostkę", "powiedz ciekawostkę", "powiedz coś ciekawego",
              "podaj jakąś ciekawostkę", "powiedz ciekawostkę"]
JOKES_WAKE = ["suchar", "opowiedz dowcip", "powiedz dowcip", "powiedz żart", "opowiedz kawał", "powiedz kawał",
              "opowiedz żart", "żart", "dowcip"]


def get_audio(sample_rate, chunk_size, timeout):
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
            return ""


def start_listening(frame):
    wake = "Grażyna"
    sample_rate = 48000
    chunk_size = 2048
    # mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
    # mic_list = sr.Microphone.list_microphone_names()
    #
    # for i, microphone_name in enumerate(mic_list):
    #     if microphone_name == mic_name:
    #         device_id = i

    while True:
        print("Listening")
        text = get_audio(sample_rate, chunk_size, 2)

        if text.count(wake) > 0:
            frame.assistant_listening()
            print("I am ready")
            text = get_audio(sample_rate, chunk_size, 5)
            while text == "":
                frame.assistant_doesnt_understand()
                text = get_audio(sample_rate, chunk_size, 5)
            print(text)
            frame.user_speaks(text)
            text = text.lower()
            try:
                if text in JOKES_WAKE:
                    if len(jokes.jokes) == 0:
                        frame.assistant_speaks("Chwileczkę...")
                    joke = jokes.get_random_joke()
                    frame.assistant_speaks(joke['first_part'])
                    time.sleep(5)
                    frame.assistant_speaks(joke['second_part'])
                elif text in CURIO_WAKE:
                    frame.assistant_speaks(curiosities.get_random_curio()['curio'])
                elif "uruchom" in text:
                    driver = webdriver.Chrome(executable_path=r"./drivers/chromedriver80.exe")
                    driver.maximize_window()
                    driver.get("https://www.youtube.com/?hl=pl&gl=PL")
                    json_parser.parse_json("./json_files/yt.json", driver, text.replace('uruchom', '').upper())
                elif "pogoda" in text:
                    frame.assistant_speaks(weather.check_weather(text))
                elif "stop" in text:
                    break
                else:
                    result = wikipedia.search_in_wikipedia(text)
                    if result is not None:
                        frame.assistant_speaks(result)
            except Exception as e:
                pass



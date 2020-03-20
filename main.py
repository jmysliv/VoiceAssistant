import SpeechRecognition as sr
import jokes
import curiosities

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
    # listens for the user's input
    audio = r.listen(source, timeout=2)

    try:
        text = r.recognize_google(audio, language="pl-PL")
        print("you said: " + text)


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service;{0}".format(e))

if text == "suchar":
    jokes.get_jokes()

if text == "ciekawostki":
    curiosities.get_curiosities()

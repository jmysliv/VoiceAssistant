import speech_recognition as sr
import pyaudio
from UI.main import isLinux
if isLinux:
    default_device_index = pyaudio.PyAudio().get_default_output_device_info()['index']
else:
    default_device_index = 0


def get_audio(timeout, sample_rate=48000, chunk_size=2048):
    r = sr.Recognizer()
    with sr.Microphone(device_index=default_device_index, sample_rate=sample_rate, chunk_size=chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=timeout)
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

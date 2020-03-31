from gtts import gTTS
import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def insert_newlines(string, every=64):
    lines = []
    i = 0
    while i < len(string):
        if i + every > len(string):
            lines.append(string[i:i + every])
            i += every
        else:
            offset = find_blank(string[i:i + every])
            lines.append(string[i:i + offset])
            i += offset
    return '\n'.join(lines)


def find_blank(string):
    print(string)
    for i in range(len(string) - 1, 0, -1):
        if string[i] is " ":
            return i
    return 1

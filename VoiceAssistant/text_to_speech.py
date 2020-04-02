import re
import pyttsx3


def speak(text):
    text = remove_brackets(text)
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(e)


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
    for i in range(len(string) - 1, 0, -1):
        if string[i] is " ":
            return i
    return 1


def remove_brackets(text):
    return re.sub("[\(\[].*?[\)\]]", "", text)

Voice Assistant :information_desk_person::sound:
===
*Project created as a part of the subject 'Programming in Python' in AGH University of Science and Technology.*

## Team :punch:

+ [Jakub Myśliwiec](https://github.com/jmysliv):airplane::bomb:
+ [Sebastian Kuśnierz](https://github.com/skusnierz) :fire:

## About Project :question:

Our idea was to create voice assistant similar to Google assistant but for desktop devices and in polish language. We decided that assistant will have the following features:

+ [telling jokes](###telling-jokes) :joy:
+ [finding curiosities](###finding-curiosities) :mortar_board:
+ [playing YouTube videos](###playing-YouTube-videos) :tv:
+ [searching phrase in both Wikipedia and Google](###searching-phrase-in-both-Wikipedia-and-Google) :mag_right:
+ [checking current Covid-19 data](###checking-current-Covid-19-data) :skull:
+ [planning events](###planning-events) :date:
+ [sending and receiving messages with other users](###sending-and-receiving-messages-with-other-users) :incoming_envelope:
+ [planning tasks](###planning-tasks) :calendar:
+ [changing volume](###changing-volume) :mute:
+ [checking current weather](###checking-current-weather) :cloud:
+ [changing brightness of the screen](###changing-brightness-of-the-screen) :high_brightness:

During implementation we used many libraries and frameworks, for instance:

+ Django REST Framework to implement dedicated server
+ Selenium for automating web browsers
+ Google speech recognition
+ Tkinter for creating graphical user interface

While working on the project we learned how to properly configure python virtual environment, so we could use it easily with operating systems both Ubuntu and Windows. New experience for us was to create REST API server using Django framework. We've had experience with REST API architecture before, but in different programming languages, so it was our first time with Django. We have also learned a lot about group cooperation, and sharing responsibilities.

## Get Started :rocket:

### Install requirements :mega:
All necessary libraries and packages are in file [requirements.txt](VoiceAssistant/requirements.txt)  
Before running command below make sure that you have installed Python 3.7+ :snake: and you are in folder with [requirements.txt](VoiceAssistant/requirements.txt)
#### Windows :poop:
```bash
    cd VoiceAssistant
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements_windows.txt
    pipwin install pyaudio
    cd UI
    ../venv/Scripts/python main.py
```
#### Linux :ok_hand:

```bash
    cd VoiceAssistant
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements_linux.txt
    cd UI
    ../venv/bin/python3 main.py
```
## User Guide

*Here you can find information how to proper interact with our assistant, and what command is responsible for what feature.*

### Telling jokes
*TO DO*
### Finding curiosities
*TO DO*
### Playing YouTube videos
*TO DO*
### Searching phrase in both Wikipedia and Google
*TO DO*
### Checking current Covid-19 data
*TO DO*
### Planning events
*TO DO*
### Sending and receiving messages with other users
*TO DO*
### Planning tasks
*TO DO*
### Changing volume
*TO DO*
### Checking current weather
*TO DO*
### Changing brightness of the screen
*TO DO*
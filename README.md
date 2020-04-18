Voice Assistant :information_desk_person::sound:
===
*Project created as a part of the subject 'Programming in Python' in AGH University of Science and Technology.*

## Team :punch:

+ [Jakub Myśliwiec](https://github.com/jmysliv):airplane::bomb:
+ [Sebastian Kuśnierz](https://github.com/skusnierz) :fire:

## About Project :question:

Our idea was to create voice assistant similar to Google assistant but for desktop devices and in polish language. We decided that assistant will have the following features:

+ [telling jokes](#joke) :joy:
+ [finding curiosities](#curiosities) :mortar_board:
+ [playing YouTube videos](#yt) :tv:
+ [searching phrase in both Wikipedia and Google](#wiki) :mag_right:
+ [checking current COVID-19 data](#covid) :skull:
+ [planning events](#events) :date:
+ [sending and receiving messages with other users](#message) :incoming_envelope:
+ [planning tasks](#tasks) :calendar:
+ [changing volume](#volume) :mute:
+ [checking current weather](#weather) :cloud:
+ [changing brightness of the screen](#brightness) :high_brightness:

During implementation we used many libraries and frameworks, for instance:

+ Django REST Framework to implement dedicated server
+ Selenium for automating web browsers
+ Google speech recognition
+ Tkinter for creating graphical user interface

While working on the project we learned how to properly configure python virtual environment, so we could use it easily with operating systems both Ubuntu and Windows. New experience for us was to create REST API server using Django framework. We've had experience with REST API architecture before, but in different programming languages, so it was our first time with Django. We have also learned a lot about group cooperation, and sharing responsibilities.

## Get Started :rocket:

### Install requirements :mega:
All necessary libraries and packages are in file [requirements_windows.txt](VoiceAssistant/requirements_windows.txt) for windows operating system and in  [requirements_linux.txt](VoiceAssistant/requirements_linux.txt) for Linux.  
Before running command below make sure that you have installed Python 3.7+ :snake: and you are in folder with requirement files.

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
## User Guide :heavy_exclamation_mark:

*Here you can find information how to proper interact with our assistant, and what command is responsible for what feature.*

### Telling jokes <a id="joke"></a> :joy:
*TO DO*
### Finding curiosities <a id="curiosities"></a> :mortar_board:
*TO DO*
### Playing YouTube videos <a id="yt"></a>  :tv:
*TO DO*
### Searching phrase in both Wikipedia and Google <a id="wiki"></a> :mag_right:
*TO DO*
### Checking current COVID-19 data <a id="covid"></a> :skull:
*TO DO*
### Planning events  <a id="events"></a> :date:
*TO DO*
### Sending and receiving messages with other users  <a id="message"></a> :incoming_envelope:
*TO DO*
### Planning tasks  <a id="tasks"></a> :calendar:
*TO DO*
### Changing volume  <a id="volume"></a> :mute:
*TO DO*
### Checking current weather  <a id="weather"></a> :cloud:
*TO DO*
### Changing brightness of the screen <a id="brightness"></a> :high_brightness:
*TO DO*
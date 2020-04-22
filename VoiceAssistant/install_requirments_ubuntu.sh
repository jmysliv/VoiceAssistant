#!/bin/bash
cd VoiceAssistant
python3 -m venv venv
source venv/bin/activate
pip install wheel
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg libav-tools
sudo apt-get update & sudo apt-get install espeak & sudo apt-get install python3-tk
pip install -r requirements_linux.txt
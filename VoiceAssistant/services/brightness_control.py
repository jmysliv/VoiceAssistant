import time
from command_manager import get_audio
from UI.main import isLinux
if isLinux:
    import os
else:
    import pythoncom
    pythoncom.CoInitialize()
    import wmi


def set_brightness(brightness):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)


def get_wake_words():
    return ["jasność", "kontrast"]


def wake_function(frame, *rest):
    frame.assistant_speaks("Na ile mam ustawić kontrast?")
    time.sleep(1.5)
    brightness = get_audio(5)
    while brightness == "":
        frame.assistant_doesnt_understand()
        brightness = get_audio(5)
    frame.user_speaks(brightness)
    if isLinux:
        connected_displays = os.popen('xrandr | grep " connected" | cut -f1 -d " "').read()
        os.system(
            "xrandr --output {} --brightness {}".format(connected_displays.splitlines()[0], float(int(brightness) / 100)))
    else:
        set_brightness(int(brightness))
    frame.assistant_speaks("Zrobione")

import time
from command_manager import get_audio
import platform
from UI.main import isLinux
if isLinux:
    import alsaaudio
    import os
else:
    import services.system_control_windows as sc_win


def volume_wake_function(frame, *rest):
    frame.assistant_speaks("Na ile mam ustawić głośności?")
    time.sleep(1.5)
    volume = get_audio(5)
    while volume == "":
        frame.assistant_doesnt_understand()
        volume = get_audio(5)
    frame.user_speaks(volume)
    if isLinux:
        m = alsaaudio.Mixer()
        m.setvolume(int(volume))
    else:
        sc_win.set_volume(int(volume))
    frame.assistant_speaks("Zrobione")


def brightness_wake_function(frame, *rest):
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
        sc_win.set_brightness(int(brightness))
    frame.assistant_speaks("Zrobione")

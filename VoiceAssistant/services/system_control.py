import time
import ctypes
import wmi
from command_manager import get_audio
import platform
isLinux = 'Linux' == platform.system()
if isLinux:
    import alsaaudio
    import os

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBoardInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time",ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBoardInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]


class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]


VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF


def key_down(keyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput(keyCode, 0x48, 0, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def key_up(keyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput(keyCode, 0x48, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def key(key_code, length = 0):
    key_down(key_code)
    time.sleep(length)
    key_up(key_code)


def volume_up():
    key(VK_VOLUME_UP)


def volume_down():
    key(VK_VOLUME_DOWN)


def set_volume(volume):
    for i in range(0, 50):
        volume_down()
    for i in range(int(volume / 2)):
        volume_up()


def set_brightness(brightness):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)


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
        set_volume(int(volume))
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
            "xrandr --output {} --brightness {}".format(connected_displays.splitlines()[0], float(brightness / 100)))
    else:
        set_brightness(int(brightness))
    frame.assistant_speaks("Zrobione")

import time
from command_manager import get_audio
from UI.main import isLinux
if isLinux:
    import alsaaudio
else:
    import ctypes
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


def get_wake_words():
    return ["głośność", "przycisz", "podgłośni", "dźwięk"]


def wake_function(frame, *rest):
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


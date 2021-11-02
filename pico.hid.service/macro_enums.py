from enum import Enum

class Order(Enum):
    """
    Pre-defined orders
    """
    HELLO = 0
    SERVICE_READY = 1
    DEVICE_READY = 2
    RESTART_BOARD = 3
    ERROR = 4
    RECEIVED = 5
    STOP = 6
    SET_COLOR = 14
    SHORT_PRESSED = 15
    SET_BLINK_COLOR = 16
    SET_MULTI_COLOR = 17

class Action(Enum):
    RUN_PROGRAM = 0
    SWAP_LAYOUT = 1
    SOUND_MIXER = 2
    PLAY_SOUND = 3
    PASTE_SENSITIVE_INFORMATION = 4
    INPUT = 5
    TIME_JOURNAL = 6

class InterProcessCommunication(Enum):
    RESTART_BACKGROUND_SERVICE = 0
    RESTART_TRAY_ICON = 1
    PROCESS_INFO = 2
    REQUEST_RESTART_MACROPAD = 3
    CHANGED_PASSWORD = 4
    CHANGED_PASSWORD_SUCCESSFUL = 5

class Color(Enum):
    RED = '0xff0000'
    GREEN = '0x00ff00'
    BLUE = '0x0000ff'
    LIGHTBLUE = '0x333388'
    WHITE = '0xffffff'
    BLACK = '0x000000'
    INDIGO = '0x4b0082'
    VIOLET = '0x8f00ff'
    CLEAR = '0x080808'
    YELLOW = '0xffff00'
    ORANGE = '0xffa500'
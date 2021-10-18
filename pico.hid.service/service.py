from layout_manager import LayoutManager
from serial import Serial, SerialException, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
import time
from enum import Enum
from layout_manager import LayoutManager
from settings import Settings
from sound_mixer import SoundMixer, MixerCommand
from password_manager import PasswordManager
from keyboard_manager import KeyboardManager
import subprocess
import os.path
import pyperclip
import getpass

settings = Settings()
layoutManager = LayoutManager()
soundMixer = SoundMixer(settings)
passwordManager = PasswordManager()
keyboardManager = KeyboardManager()

isDeviceReady = False
isDeviceConnected = False
refreshRate = 1

class Order(Enum):
    """
    Pre-defined orders
    """
    HELLO = 0
    SERVICE_READY = 1
    DEVICE_READY = 2
    ALREADY_CONNECTED = 3
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

def run_program(path):
    subprocess.call([path])

def build_message(command, *args):
    message = get_hexdata(command)
    for arg in args:
        hexarg = get_hexdata(arg[0], arg[1])
        message += f" {hexarg}"
    return f"{message}\r"

def get_hexdata(base10, padding=2):
    return "0x%0*X" % (padding,base10)

def set_color(key, color):
    reply = build_message(Order.SET_COLOR.value, (key, 2), (int(color, 0),6))
    send_message(bytes(reply, encoding='utf-8'))

def set_multi_color(colorstrings):
    reply = build_message(Order.SET_MULTI_COLOR.value, *[(int(Color[colorstrings[i]].value, 0), 6) for i in colorstrings])
    send_message(bytes(reply, encoding='utf-8'))

def set_blink_color(key, color, interval):
    reply = build_message(Order.SET_BLINK_COLOR.value, (key, 2), (int(color, 0),6), (interval,3))
    send_message(bytes(reply, encoding='utf-8'))

def set_base_colors():
    keycolors = layoutManager.getBaseColors()
    set_multi_color(keycolors)
    #for k in keycolors.keys():
    #    set_color(k, Color[keycolors[k]].value)

def exec_establish_connection(command):
    global isDeviceReady
    if command == Order.HELLO:
        reply = build_message(Order.SERVICE_READY.value)
        send_message(bytes(reply,encoding='utf-8'))
    elif command == Order.DEVICE_READY:
        isDeviceReady = True
        set_base_colors()
        

def exec_command(command, payload):
    args = payload.split()

    key = None
    if len(args) > 0:
        key = int(args[0], 16)
    action = layoutManager.getAction(command, key)
    if action == None or command == Order.HELLO or command == Order.DEVICE_READY:
        return
    if action['type'] == Action.RUN_PROGRAM.name:
        run_program(action['program'])
    elif action['type'] == Action.SWAP_LAYOUT.name:
        layoutManager.swapLayout(action['direction'])
        set_base_colors()
    elif action['type'] == Action.SOUND_MIXER.name:
        command = action['command']
        keycolors = layoutManager.getBaseColors()
        colorStr = keycolors[key]
        if command == MixerCommand.MIC_MUTE.name:
            colorStr = action['toggleColors']['onColor']
            if soundMixer.IsMuted:
                colorStr = action['toggleColors']['offColor']
        elif command == MixerCommand.SOUND_MUTE.name:
            colorStr = action['toggleColors']['onColor']
            if soundMixer.IsSoundMuted:
                colorStr = action['toggleColors']['offColor']
        elif command == MixerCommand.MUSIC_TOGGLE_PLAY.name:
            colorStr = action['toggleColors']['offColor']
            if soundMixer.isMusicPlaying():
                colorStr = action['toggleColors']['onColor']
        elif command == MixerCommand.MUSIC_TOGGLE_MUTE.name:
            colorStr = action['toggleColors']['onColor']
            if soundMixer.isMusicMuted():
                colorStr = action['toggleColors']['offColor']
        elif command == MixerCommand.PLAY_FILE.name:
            set_blink_color(key, Color[keycolors[key]].value, 150)
        soundMixer.execCommand(action, lambda: set_color(key, Color[colorStr].value))
    elif action['type'] == Action.PASTE_SENSITIVE_INFORMATION.name:
        sens_val = passwordManager.get_password(action['password_name'])
        pyperclip.copy(sens_val)
        keyboardManager.sendPaste()

def process_callback(action, key):
    type = action['type']
    if type == Action.SOUND_MIXER.name:
        command = action['command']
        colorStr = action['toggleColors']['offColor']
        if command == MixerCommand.MIC_MUTE.name:
            if soundMixer.IsMuted:
                colorStr = action['toggleColors']['onColor']
        elif command == MixerCommand.SOUND_MUTE.name:
            if soundMixer.IsSoundMuted:
                colorStr = action['toggleColors']['onColor']
        set_color(key, Color[colorStr].value)

def send_message(payload):
    ser.write(payload) 
    ser.flush()
    time.sleep(0.00)

def parseCommand(command):
    return Order(int(command, 0))

def parseInput(rawData):
    data = rawData.decode('utf-8')
    if data[:2] == '0x':
        command = parseCommand(data[:4])
        if isDeviceReady:
            exec_command(command, data[4:])
        else:
            exec_establish_connection(command)

def connect():
    global isDeviceConnected
    global refreshRate
    serialPort = settings.getSetting('device_com_port')
    while not isDeviceConnected:
        time.sleep(3)
        try:
            print(f"Connecting to port '{serialPort}...'")
            ser = Serial(
                port=serialPort, 
                baudrate=9600,
                parity=PARITY_NONE,
                stopbits=STOPBITS_ONE,
                bytesize=EIGHTBITS,
                timeout=1)
            isDeviceConnected = True
            refreshRate = 0.01
        except PermissionError as e:
            print(e.strerror)
        except (SerialException, FileNotFoundError) as e:
            print(f"Cannot find device on Port '{serialPort}'")
        except Exception as e:
            print(e)
    print(f"Successfully connected to device on port '{serialPort}'")
    return ser

passwordfile = "passwords.encrypted"
if not os.path.isfile(passwordfile):
    print( "Set Password to encrypt passwordfile (must be named 'passwords.json'):")
    pw = input()
    passwordManager.encrypt_file("passwords.json", pw)

print( "Decrypt passwordfile")
pw = getpass.getpass()
passwordManager.decrypt_file(passwordfile, pw)


ser = connect()
reply = b''

while True:
    try:
        bytestoread = ser.inWaiting()
        if bytestoread != 0:
            reply = ser.readline().strip()
            parseInput(reply)
    except:
        isDeviceConnected = False
        refreshRate = 1
        ser = connect()

from layout_manager import LayoutManager
import serial
import time
from enum import Enum
from layout_manager import LayoutManager
from sound_mixer import SoundMixer, MixerCommand
import subprocess

layoutManager = LayoutManager()
soundMixer = SoundMixer()

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
    SHORT_PRESSED = 15
    SET_COLOR = 14

class Action(Enum):
    RUN_PROGRAM = 0
    SWAP_LAYOUT = 1
    SOUND_MIXER = 2
    PLAY_SOUND = 3

class Color(Enum):
    RED = '0xff0000'
    GREEN = '0x00ff00'
    BLUE = '0x0000ff'
    WHITE = '0xffffff'
    BLACK = '0x000000'
    INDIGO = '0x4b0082'
    VIOLET = '0x8f00ff'
    CLEAR = '0x080808'
    YELLOW = '0xffff00'
    ORANGE = '0xffa500'

def run_program(path):
    subprocess.call([path])

def get_hexcommand(command):
    padding = 2
    return "0x%0*X" % (padding,command)

def set_color(key, color):
    reply = f"{get_hexcommand(Order.SET_COLOR.value)}{key:02}{int(color, 0)}\r"
    send_message(bytes(reply, encoding='utf-8'))

def exec_establish_connection(command):
    global isDeviceReady
    if command == Order.HELLO:
        reply = f"{get_hexcommand(Order.SERVICE_READY.value)}00000\r"
        send_message(bytes(reply,encoding='utf-8'))
    elif command == Order.DEVICE_READY:
        isDeviceReady = True
        keycolors = layoutManager.getBaseColors()
        for k in keycolors.keys():
            set_color(k, Color[keycolors[k]].value)

def exec_command(command, payload):
    key = int(payload, 16)
    action = layoutManager.getAction(command, key)
    if action == None or command == Order.HELLO or command == Order.DEVICE_READY:
        return
    if action['type'] == Action.RUN_PROGRAM.name:
        run_program(action['program'])
    elif action['type'] == Action.SWAP_LAYOUT.name:
        print("dummy swap")
    elif action['type'] == Action.SOUND_MIXER.name:
        soundMixer.execCommand(action)
    process_callback(action, key)

def process_callback(action, key):
    type = action['type']
    if type == Action.SOUND_MIXER.name:
        command = action['command']
        if command == MixerCommand.PLAY_FILE.name:
            return


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
    while not isDeviceConnected:
        try:
            ser = serial.Serial('COM7', baudrate=115200, timeout=0.1)
            isDeviceConnected = True
            refreshRate = 0.01
        except:
            time.sleep(1)
            pass
    return ser


ser = connect()
reply = b''

while True:
    try:
        a = ser.read()
    except:
        isDeviceConnected = False
        refreshRate = 1
        ser = connect()

    if a== b'\r' and ser.read()==b'\n':
        parseInput(reply)
        reply = b''
    else:
        reply += a

    time.sleep(refreshRate)

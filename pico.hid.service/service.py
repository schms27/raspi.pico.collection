from layout_manager import LayoutManager
import serial
import time
from enum import Enum
from layout_manager import LayoutManager
from sound_mixer import SoundMixer
import subprocess

layoutManager = LayoutManager()
soundMixer = SoundMixer()

class Order(Enum):
    """
    Pre-defined orders
    """
    HELLO = 0
    SERVO = 1
    MOTOR = 2
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

class Color(Enum):
    RED = '0xff0000'
    GREEN ='0x00ff00'
    BLUE ='0x0000ff'

def run_program(path):
    subprocess.call([path])

def get_hexcommand(command):
    padding = 2
    return "0x%0*X" % (padding,command)

def set_color(key, color):
    reply = f"{get_hexcommand(Order.SET_COLOR.value)}{key:02}{int(color, 0)}\r"
    send_message(bytes(reply, encoding='utf-8'))

def exec_command(command, payload):
    key = int(payload)
    action = layoutManager.getAction(command, key)
    if action == None:
        return
    if action['type'] == Action.RUN_PROGRAM.name:
        run_program(action['program'])
    elif action['type'] == Action.SWAP_LAYOUT.name:
        print("dummy swap")
    elif action['type'] == Action.SOUND_MIXER.name:
        command = action['command']
        print(f"sound mixer {command}")
        soundMixer.execCommand(command)
        set_color(key, Color.RED.value)



def send_message(payload):
    ser.write(payload) 

def parseCommand(command):
    return Order(int(command, 0))

def parseInput(rawData):
    data = rawData.decode('utf-8')
    print(f"decoded reply: {data}")
    if data[:2] == '0x':
        command = parseCommand(data[:4])
        exec_command(command, data[4:])

ser = serial.Serial(
             'COM3',
             baudrate=115200,
             timeout=0.1)

reply = b''

while True:
    a = ser.read()

    if a== b'\r' and ser.read()==b'\n':
        parseInput(reply)
        reply = b''
    else:
        reply += a

    time.sleep(0.01)

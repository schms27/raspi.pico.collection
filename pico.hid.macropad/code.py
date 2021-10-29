import time
import board
import busio
import usb_hid
import supervisor

from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from digitalio import DigitalInOut, Direction, Pull


#from robust_serial import Order, write_order, write_i8, write_i16
#from robust_serial.utils import open_serial_port

# Open serial port with a baudrate of 9600 (bits/s)
#serial_file = open_serial_port(baudrate=9600)

#------------------------------------
from constants import *
from keypad import *
from keyconfig.send_keys import *
#------------------------------------
for _ in range(10):
    print(" ")
print("  ============ NEW EXECUTION ============  ")
#------------------------------------
interfaces = [ SerialKeypad ]
currentInterface = -1
#------------------------------------

# CS  : GP17 - 22
# SCLK: GP18 - 24
# MOSI: GP19 - 25
# ----- I2C -----
# INT : GP3  - 05 ? Not used!
# SDA : GP4  - 06
# SCL : GP5  - 07
cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, BUTTON_COUNT, brightness=0.2, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
#------------------------------------
picoLED = DigitalInOut(board.GP25)
picoLED.direction = Direction.OUTPUT
picoLED.value = 0
#------------------------------------
timeDown = [-1] * BUTTON_COUNT
timeUp = [-1] * BUTTON_COUNT
waiting = [False] * BUTTON_COUNT
keypadButtonStates = [ timeDown, timeUp, waiting ]
#------------------------------------

blink_buttons = []

def setKeyColour(pixel, colour):
    pixels[pixel] = (((colour >> 16) & 255), (colour >> 8) & 255, colour & 255)

def swapLayout():
    global currentKeypadConfiguration
    global currentInterface
    currentInterface = (currentInterface + 1) % len(interfaces)
    currentKeypadConfiguration = interfaces[currentInterface](kbd, layout, setKeyColour)
    currentKeypadConfiguration.introduce()

def read_button_states(x, y):
    pressed = [0] * BUTTON_COUNT
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8
        for i in range(x, y):
            if not (1 << i) & b:
                pressed[i] = 1
            else:
                pressed[i] = 0
    return pressed
#------------------------------------
def checkHeldForFlash(heldDownStartMillis):
    if heldDownStartMillis > 0:
        downTime = timeInMillis() - heldDownStartMillis
        picoLED.value = (downTime >= LONG_HOLD and downTime <= LONG_HOLD + 100) or (downTime >= EXTRA_LONG_HOLD and downTime <= EXTRA_LONG_HOLD + 100)
    else:
        picoLED.value = 0


def exec_command(command, payloadRaw):
    print(payloadRaw)
    if command == 1:
        currentKeypadConfiguration.sendSerial(-1, 2)
        currentKeypadConfiguration.isServiceReady = True
    if command == 3:
        currentKeypadConfiguration.handleExtraLongPress(0)
    if command == 14:
        key = int(payloadRaw[0])
        color = int(payloadRaw[1])
        try:
            blink_conf = next(item for item in blink_buttons if item["key"] == key)
            blink_buttons.remove(blink_conf)
        except:
            pass
        setKeyColour(key, color)
    if command == 16:
        blink_buttons.append({"key":int(payloadRaw[0], 16), "color":int(payloadRaw[1], 16), "interval":int(payloadRaw[2], 16), "state_on":True, "last_handled":0})
    if command == 17:
        for key, c in enumerate(payloadRaw):
            color = int(c)
            try:
                blink_conf = next(item for item in blink_buttons if item["key"] == key)
                blink_buttons.remove(blink_conf)
            except:
                pass
            setKeyColour(key, color)


def parseCommand(command):
    return int(command, 0)


def parse_data(rawData):
    command = parseCommand(rawData[:4])
    exec_command(command, rawData[4:].split())

def serial_read():
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        parse_data(value)

def handle_button_blink():
    global last_handled_time
    global blink_buttons
    current_mono_time = time.monotonic_ns() / 1e6
    for blink_conf in blink_buttons:
        delta_time = current_mono_time - blink_conf["last_handled"]
        if delta_time > blink_conf["interval"]:
            print(blink_conf)
            if not blink_conf["state_on"]:
                setKeyColour(blink_conf["key"], blink_conf["color"])
                blink_conf["state_on"] = True
            else:
                pass
                setKeyColour(blink_conf["key"], 0)
                blink_conf["state_on"] = False
            blink_conf["last_handled"] = current_mono_time
        
#------------------------------------
currentKeypadConfiguration = KeypadInterface(kbd, layout, setKeyColour)
currentKeypadConfiguration.introduce()
#------------------------------------
helpMode=False


swapLayout()
loop_counter = 0
while True:
    serial_read()

    currentKeypadConfiguration.loop()

    pressed = read_button_states(0, BUTTON_COUNT)

    for keyIndex in range(BUTTON_COUNT):
        event = checkButton(keyIndex, pressed[keyIndex], keypadButtonStates, checkHeldForFlash)
        if helpMode:
            print(currentKeypadConfiguration.helpForKey(keyIndex))
            helpMode = False
        else:
            currentKeypadConfiguration.handleEvent(keyIndex, event)

    handle_button_blink()
    loop_counter += 1
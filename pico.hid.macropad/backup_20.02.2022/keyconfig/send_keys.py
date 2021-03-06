import time
import microcontroller
from constants import *
from adafruit_hid.keycode import Keycode

class SerialKeypad():
    #--- OPTIONAL METHODS ---

    def teamsIntro(self, frame):
        if frame >= 4:
            return
        for row in range(4):
            index = (frame * 4) + row
            self.setKeyColour(index, self.IMAGE[index])

    def teamsMicToggle(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.M)
    def teamsCameraToggle(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.O)
    def teamsHangUp(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.B)
    def get_hexdata(self, base10, padding=2):
        return "0x%0*X" % (padding,base10)
    def build_message(self, command, *args):
        message = self.get_hexdata(command)
        for arg in args:
            if arg[0] == -1:
                continue
            hexarg = self.get_hexdata(arg[0], arg[1])
            message += f" {hexarg}"
        return f"{message}\r"
    def sendSerial(self, key, command):
        print(self.build_message(command, (key, 2)))
        time.sleep(0.01)

    def handleExtraLongPress(self, key):
        if key == 0:
            microcontroller.reset()

    #------------------------
    #--- REQUIRED METHODS ---
    IMAGE = [
            COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE,
            COLOUR_WHITE, COLOUR_INDIGO, COLOUR_INDIGO, COLOUR_INDIGO,
            COLOUR_WHITE, COLOUR_WHITE, COLOUR_INDIGO, COLOUR_WHITE,
            COLOUR_WHITE, COLOUR_WHITE, COLOUR_INDIGO, COLOUR_WHITE
        ]

    def loop(self):
        if not self.isServiceReady and self.loopCounter % 100 == 0:
            self.sendSerial(0, 0)
        self.loopCounter += 1

    def getKeyColours(self):
        return (
            (darkVersion(self.IMAGE[0]),  COLOUR_ORANGE),
            (darkVersion(self.IMAGE[1]),  COLOUR_BLUE),
            (darkVersion(self.IMAGE[2]),  COLOUR_RED),
            (darkVersion(self.IMAGE[3]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[4]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[5]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[6]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[7]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[8]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[9]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[10]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[11]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[12]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[13]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[14]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[15]), COLOUR_YELLOW)
        )

    def __init__(self, keyboard, keyboardLayout, setKeyColour):
        self.setKeyColour = setKeyColour
        self.keyboard = keyboard
        self.keyboardLayout= keyboardLayout
        self.isServiceReady = False
        self.loopCounter = 0

    def introduce(self):
        self.resetColours(COLOUR_OFF)
        self.startAnimationTime = timeInMillis()
        self.currentFrame = -1
        self.maxFrame = 4
        self.frameIndex = 0

    def resetColours(self, colours):
        for key in range(BUTTON_COUNT):
            if isinstance(colours, int):
                self.setKeyColour(key, colours)
            elif len(colours) == BUTTON_COUNT:
                self.setKeyColour(key, colours[key][0])

    def handleEvent(self, index, event):
        if event & EVENT_EXTRA_LONG_PRESS:
            self.handleExtraLongPress(index)
        if event & EVENT_SINGLE_PRESS:
            self.sendSerial(index, 15)
    #------------------------

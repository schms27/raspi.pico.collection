import win32api
import time
from threading import Thread
from enum import Enum
import numpy as np
from random import randint
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from logging import debug, warning
import pyperclip

from macro_enums import Color

class InputCommand(Enum):
    MOVE_MOUSE = 0
    TYPE_KEY = 1
    MOVE_MOUSE_RANDOM = 2

class InputManager():
    def __init__(self, calling_app = None):
        # self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1) 
        self.isAutoMouseMove = False  
        self.currentAnimationTime = 0
        self.lastAnimationUpdateTime = 0
        self.animationStartTime = 0
        self.timestep = 100 #refresh every 100 millis
        self.callingApp = calling_app

    def sendPaste(self):
        t = Thread(target=self.sendKeys, args=(Key.ctrl.value, 'v'))
        t.start()
        # self.keyboard.press(Key.ctrl.value)
        # self.keyboard.press('v')
        # self.keyboard.release('v')
        # self.keyboard.release(Key.ctrl.value)

    def sendKeys(self, **keys):
        keyboard = KeyboardController()
        for key in keys:
            keyboard.press(key)
        for key in keys:
            keyboard.release(key)

    def clear_clipboard(self):
        pyperclip.copy('')

    def moveMouseTo(self, x, y):
        debug(f"current mouse position is: {self.mouse.position}")
        try:
            self.mouse.position = (x, y)
        except Exception as e:
            warning(f"error occured while trying to move mouse to {(x, y)}: {e}")
        debug(f"new mouse position is: {(x, y)}")

    def loop(self):
        if self.isAutoMouseMove:
            if not hasattr(self, 'nextMoves') or len(self.nextMoves) == 0:
                self.nextMoves = self.getNextMouseMovements()

            self.currentAnimationTime = (time.time_ns() // 1_000_000) - self.animationStartTime
            if self.currentAnimationTime - self.lastAnimationUpdateTime >= self.timestep:
                new_mouse_pos = self.nextMoves.pop(0)
                self.moveMouseTo(new_mouse_pos[0], new_mouse_pos[1])
                self.lastAnimationUpdateTime = self.currentAnimationTime

    def toggleRandomMouseMovement(self):
        if self.isAutoMouseMove:
            self.lastAnimationUpdateTime = self.animationStartTime = 0
            self.isAutoMouseMove = False
        else:
            self.isAutoMouseMove = True
            self.animationStartTime = time.time_ns() // 1_000_000 

    def getNextMouseMovements(self) -> list:
        targetCoord = next(self.generateRandomCoordinate(self.screen_width-10, self.screen_height-10))
        return self.createIntermediateCoordinates(self.mouse.position, targetCoord, randint(500, 5000))

    def createIntermediateCoordinates(self, startCoord, targetCoord, duration):
        dir = np.array(targetCoord) - np.array(startCoord)
        numOfIntermediates = duration / self.timestep
        intermediateCoordinates = []

        for i in range(int(numOfIntermediates)):
            intermediateCoordinates.append(np.array(startCoord) + (dir * i * (self.timestep / duration)))
        return intermediateCoordinates

    def generateRandomCoordinate(self, max_x, max_y, min_x=10, min_y=10 ):
        seen = set()
        x, y = randint(min_x, max_x), randint(min_y, max_y)
        while True:
            seen.add((x, y))
            yield (x, y)
            x, y = randint(min_x, max_x), randint(min_y, max_y)
            while (x, y) in seen:
                x, y = randint(min_x, max_x), randint(min_y, max_y)

    def execCommand(self, action, key):
        command = action['command']
        if command == InputCommand.MOVE_MOUSE.name:
            self.moveMouseTo(action['x'], action['y'])
        elif command == InputCommand.MOVE_MOUSE_RANDOM.name:
            self.toggleRandomMouseMovement()
            if self.isAutoMouseMove:
                blink_color = action['active_color']
                self.callingApp.set_blink_color(key, Color[blink_color].value, 150)
            else:
                basecolor = self.callingApp.layoutManager.getBaseColors()[key]
                self.callingApp.set_color(key, Color[basecolor].value)

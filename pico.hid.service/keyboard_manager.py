from pynput.keyboard import Key, Controller

class KeyboardManager():
    def __init__(self):
        self.keyboard = Controller()

    def sendPaste(self):
        self.keyboard.press(Key.ctrl.value)
        self.keyboard.press('v')
        self.keyboard.release('v')
        self.keyboard.release(Key.ctrl.value)

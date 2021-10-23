import json
from enum import Enum
from macro_enums import Order
from settings import Settings
from logging import debug

class SwapDirection(Enum):
    FORWARD = 0
    BACKWARD = 0

class LayoutManager():

    def __init__(self, settings: Settings) -> None:
        file = open(settings.getSetting('layouts_filepath'),)
        self.layoutData = json.load(file)
        self.switchLayout(0)

    def swapLayout(self, direction: str) -> None:
        newIndex = self.currentLayoutIndex - 1
        if(direction == SwapDirection.FORWARD.name):
            newIndex = self.currentLayoutIndex + 1
        self.switchLayout(newIndex % len(self.layoutData['layouts']))

        
    def switchLayout(self, layoutIndex: int) -> None: 
        self.currentLayoutIndex = layoutIndex

    def getAction(self, keycode: Order, key: int) -> str:
        if keycode == None or key == None or key == -1:
            return None
        for a in self.layoutData['layouts'][self.currentLayoutIndex]['actions']:
            try:
                if a['key'] == key and a['keycode'] == keycode.name:
                    return a['action']
            except:
                debug("requested action not found, check layout config, key: '{0}', keycode:'{1}'".format(key, keycode))

    def getBaseColors(self) -> 'dict[str, str]':
        keycolors = {}
        for c in self.layoutData['layouts'][self.currentLayoutIndex]['baseColors']:
            keycolors[c['key']] = c['color']
        return keycolors
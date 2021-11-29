import json
from enum import Enum
from macro_enums import Order
from settings import Settings
from logging import debug
from util import resolvePath

class SwapDirection(Enum):
    FORWARD = 0
    BACKWARD = 0

class LayoutManager():

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        with open(resolvePath(settings.getSetting('layouts_filepath')), 'r') as file:
            self.layoutData = json.load(file)
        self.switchLayout(0)

    def saveLayout(self) -> None:
        with open(resolvePath(self.settings.getSetting('layouts_filepath')), 'w') as file:
            json.dump(self.layoutData, file, ensure_ascii=False, indent=4)

    def swapLayout(self, direction: str) -> None:
        newIndex = self.currentLayoutIndex - 1
        if(direction == SwapDirection.FORWARD.name):
            newIndex = self.currentLayoutIndex + 1
        self.switchLayout(newIndex % len(self.layoutData['layouts']))

    def getCurrentLayoutName(self) -> str:
        return self.layoutData['layouts'][self.currentLayoutIndex]['name']

    def setCurrentLayoutName(self, name: str) -> str:
        self.layoutData['layouts'][self.currentLayoutIndex]['name'] = name

    def switchLayout(self, layoutIndex: int) -> None: 
        self.currentLayoutIndex = layoutIndex

    def getAction(self, key: int, keycode: Order = None):
        result = []
        if key == None or key == -1:
            return None
        for a in self.layoutData['layouts'][self.currentLayoutIndex]['actions']:
            try:
                if a['key'] == key:
                    if keycode != None:
                        if a['keycode'] == keycode.name:
                            return a['action']
                    else:
                        result.append(a)
            except:
                debug("requested action not found, check layout config, key: '{0}', keycode:'{1}'".format(key, keycode))
        return result

    # def getAction(self, key: int) -> dict:
    #     result = {}
    #     if key != None or key > -1:
    #         for a in self.layoutData['layouts'][self.currentLayoutIndex]['actions']:
    #             try:
    #                 if a['key'] == key:
    #                     result[a['keycode']] = a
    #             except:
    #                 debug(f"requested action not found, check layout config, key: '{key}'")
    #     return result

    def getBaseColors(self) -> 'dict[str, str]':
        keycolors = {}
        for c in self.layoutData['layouts'][self.currentLayoutIndex]['baseColors']:
            keycolors[c['key']] = c['color']
        return keycolors

    def setBaseColor(self, index, color) -> None:
        colorUpper = color.upper()
        if self.getBaseColors()[index] != colorUpper:
            self.layoutData['layouts'][self.currentLayoutIndex]['baseColors'][index]['color'] = color.upper()

    def createNewLayout(self) -> str:
        initialName = 'New Layout'
        defaultSwapAction = {
            'key':0,
            'keycode':'SHORT_PRESSED',
            'action' : {
                'type':'SWAP_LAYOUT',
                'direction':'FORWARD'
            }
        }
        newLayout = {
            'name': initialName,
            'actions': [defaultSwapAction],
            'baseColors':[ {'key':k,'color':'WHITE'} for k in range(0, 16)]
        }
        self.layoutData['layouts'].append(newLayout)

    def deleteCurrentLayout(self) -> None:
        del self.layoutData['layouts'][self.currentLayoutIndex]
        self.switchLayout(self.currentLayoutIndex - 1)
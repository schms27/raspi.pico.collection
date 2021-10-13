import json

class LayoutManager():

    def __init__(self):
        file = open('layout.json',)
        self.layoutData = json.load(file)

    def getAction(self, keycode, key):
        for a in self.layoutData['actions']:
            try:
                if a['key'] == key and a['keycode'] == keycode.name:
                    return a['action']
            except:
                print("requested action not found, check layout config, key: '{0}', keycode:'{1}'".format(key, keycode))

    def getBaseColors(self):
        keycolors = {}
        for c in self.layoutData['baseColors']:
            keycolors[c['key']] = c['color']
        return keycolors
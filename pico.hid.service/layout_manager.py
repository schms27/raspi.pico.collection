import json

class LayoutManager():

    def __init__(self):
        file = open('layout.json',)
        self.layoutData = json.load(file)

    def getAction(self, keycode, key):
        for a in self.layoutData['actions']:
            if a['key'] == key and a['keycode'] == keycode.name:
                return a['action']

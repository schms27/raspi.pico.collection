import json

class Settings():
    def __init__(self):
        file = open('settings.json',)
        self.settingsData = json.load(file)

    def getSetting(self, key):
        return self.settingsData[key]
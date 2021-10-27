import json
import os

class Settings():
    def __init__(self, settingsPath):
        with open(os.path.join(settingsPath,'settings.json'), 'r') as file:
            self.settingsData = json.load(file)

    def getSetting(self, key):
        return self.settingsData[key]

    def hasSetting(self, key):
        return key in self.settingsData
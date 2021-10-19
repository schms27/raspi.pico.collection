import json
import os

class Settings():
    def __init__(self, settingsPath):
        file = open(os.path.join(settingsPath,'settings.json'),)
        self.settingsData = json.load(file)

    def getSetting(self, key):
        return self.settingsData[key]
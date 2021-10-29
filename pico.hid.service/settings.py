import json
import os

class Settings():
    def __init__(self, settingsPath):
        self.settingsFilePath = os.path.join(settingsPath,'settings.json')
        with open(self.settingsFilePath, 'r') as file:
            self.settingsData = json.load(file)

    def getSetting(self, key):
        return self.settingsData[key]

    def setSetting(self, key, value):
        self.settingsData[key] = value

    def hasSetting(self, key):
        return key in self.settingsData

    def saveSettings(self):
        with open(self.settingsFilePath, 'w') as file:
            file.write(json.dumps(self.settingsData , indent=4))
import time
import argparse
import sys

from winservice import Winservice

from app import MacroPadApp

class MacropadService(Winservice):
    _svc_name_ = "MacroPadService"
    _svc_display_name_ = "MacroPad Service"
    _svc_description_ = "A Service for connecting to a Macropad over serial"

    def start(self):
        self.isRunning = True

    def stop(self):
        self.isRunning = False

    def handleCmdArguments(self, arguments):
        print(arguments.servicename)

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('servicename', type=str, nargs='?')
        parser.add_argument('-p', type=str, nargs='?', action='store',dest='password',help="Password to unlock file with sensitive data")
        parser.add_argument('-s', type=str, nargs='?', action='store',dest='settingspath',help="Path to where the settings.json is located")
        cmdargs = parser.parse_args(self.app_args)
        app = MacroPadApp(cmdargs, self.log)
        while self.isRunning:
            app.loop()
            time.sleep(0.1)

if __name__ == '__main__':
    MacropadService.parse_command_line()
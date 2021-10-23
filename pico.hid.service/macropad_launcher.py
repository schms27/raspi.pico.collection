import time
import argparse
import sys
import logging
from logging import handlers

from app import MacroPadApp

class MacropadLauncher():

    def __init__(self) -> None:
        self.isRunning = True
        self.setupLogger()

    def setupLogger(self) -> None:
        self.log = logging.getLogger('')
        self.log.setLevel(logging.DEBUG)
        format = logging.Formatter("%(asctime)s; %(levelname)s; %(message)s; %(module)s")

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(format)
        self.log.addHandler(ch)

        fh = handlers.TimedRotatingFileHandler("macropad.log", when='midnight', backupCount=7)
        fh.setFormatter(format)
        self.log.addHandler(fh)


    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('servicename', type=str, nargs='?')
        parser.add_argument('-p', '--password', type=str, nargs='?', action='store',dest='password',help="Password to unlock file with sensitive data")
        parser.add_argument('-s', '--settings_path', type=str, nargs='?', action='store',dest='settingspath',help="Path to where the settings.json is located")
        parser.add_argument('-l', '--log', type=str, nargs='?', action='store',dest='loglevel',help="desired loglevel")
        cmdargs, unknown = parser.parse_known_args(sys.argv)

        if cmdargs.loglevel is not None:
            numeric_level = getattr(logging, cmdargs.loglevel.upper(), None)
            self.log.setLevel(numeric_level)

        app = MacroPadApp(cmdargs)

        while self.isRunning:
            app.loop()
            time.sleep(0.1)

if __name__ == '__main__':
    launcher = MacropadLauncher()
    launcher.main()
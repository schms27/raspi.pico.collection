import time
import argparse
import sys
import os
import logging
from logging import handlers, debug
import multiprocessing
import setproctitle
from multiprocessing import Queue

from app import MacroPadApp
from tray_icon_app import TrayIconApp

class MacropadLauncher():

    def __init__(self) -> None:
        self.isRunning = True
        self.setupLogger()
        self.appName =  "MacroPad Launcher"

    def setupLogger(self) -> None:
        self.log = logging.getLogger('')
        self.log.setLevel(logging.DEBUG)
        format = logging.Formatter("%(asctime)s; %(levelname)s; %(message)s; %(module)s")

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(format)
        self.log.addHandler(ch)

        logdir = os.path.join(os.getenv('LOCALAPPDATA'), "MacropadLauncher\\")
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        fh = handlers.TimedRotatingFileHandler(os.path.join(logdir, "macropad.log"), when='midnight', backupCount=7)
        fh.setFormatter(format)
        self.log.addHandler(fh)


    def main(self):
        setproctitle.setproctitle(self.appName)
        parser = argparse.ArgumentParser()
        parser.add_argument('servicename', type=str, nargs='?')
        parser.add_argument('-p', '--password', type=str, nargs='?', action='store',dest='password',help="Password to unlock file with sensitive data")
        parser.add_argument('-s', '--settings_path', type=str, nargs='?', action='store',dest='settingspath',help="Path to where the settings.json is located")
        parser.add_argument('-l', '--log', type=str, nargs='?', action='store',dest='loglevel',help="desired loglevel")
        cmdargs, unknown = parser.parse_known_args(sys.argv)
        debug(f"Launching using cmd-args: {cmdargs}")
        if cmdargs.loglevel is not None:
            numeric_level = getattr(logging, cmdargs.loglevel.upper(), None)
            self.log.setLevel(numeric_level)

        q = Queue()

        app = MacroPadApp(vars(cmdargs), q)
        app.start()

        trayApp = TrayIconApp(q, 12)
        trayApp.start()

        trayApp.join()
        while not q.empty():
            debug(f"Result: {q.get()}")

        while trayApp.is_alive():
            pass
        app.isRunning = False



        # while self.isRunning:
        #     app.loop()
        #     if not trayApp.is_alive():
        #         self.isRunning = False
        #     time.sleep(0.1)

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    launcher = MacropadLauncher()
    launcher.main()
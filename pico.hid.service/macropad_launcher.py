from multiprocessing.context import Process
import time
import argparse
import sys
import os
import logging
import signal
from logging import handlers, debug, info, error
import multiprocessing
import setproctitle
from multiprocessing import Queue

from app import MacroPadApp
from tray_icon_app import TrayIconApp
from macro_enums import InterProcessCommunication, ProcessState, ProcessID

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


    def parseProcessCommunicationResponse(self, response):
        if response[0] == InterProcessCommunication.PROCESS_INFO:
            info(f"Process Info recieved '{response[3]}': {response[2]}")
            if response[1] == ProcessState.STARTED:
                if response[2] == ProcessID.MACROPAD_COM_BG:
                    self.process_com_queues['fromMain'].put((InterProcessCommunication.REQUEST_RESTART_MACROPAD, "", self.__class__.__name__))

        elif response[0] == InterProcessCommunication.RESTART_BACKGROUND_SERVICE:
            debug(f"restarting background process requested by class '{response[1]}'")
            self.background_app.kill()
            self.background_app = MacroPadApp(vars(self.cmdargs), self.process_com_queues, ProcessID.MACROPAD_COM_BG)
            self.background_app.start()


    def main(self):
        setproctitle.setproctitle(self.appName)
        parser = argparse.ArgumentParser()
        parser.add_argument('servicename', type=str, nargs='?')
        parser.add_argument('-p', '--password', type=str, nargs='?', action='store',dest='password',help="Password to unlock file with sensitive data")
        parser.add_argument('-s', '--settings_path', type=str, nargs='?', action='store',dest='settingspath',help="Path to where the settings.json is located")
        parser.add_argument('-l', '--log', type=str, nargs='?', action='store',dest='loglevel',help="desired loglevel")
        self.cmdargs, unknown = parser.parse_known_args(sys.argv)
        debug(f"Launching using cmd-args: {self.cmdargs}")
        if self.cmdargs.loglevel is not None:
            numeric_level = getattr(logging, self.cmdargs.loglevel.upper(), None)
            self.log.setLevel(numeric_level)

        self.process_com_queues = {"toMain":Queue(),"fromMain":Queue()}

        try:
            self.background_app = MacroPadApp(vars(self.cmdargs), self.process_com_queues, ProcessID.MACROPAD_COM_BG)
            self.background_app.start()
        except Exception as e:
            error(f"Error occured while constructing '{MacroPadApp.__name__}',{e}")
            return

        try:
            trayApp = TrayIconApp(vars(self.cmdargs), self.process_com_queues, ProcessID.TRAY_APP)
            trayApp.start()
        except Exception as e:
            error(f"Error occured while constructing '{TrayIconApp.__name__}',{e}")
            return



        # while not self.q.empty():
        #     debug(f"Result: {self.q.get()}")

        # trayApp.join()
        while trayApp.is_alive():
            if not self.process_com_queues['toMain'].empty():
                self.parseProcessCommunicationResponse(self.process_com_queues['toMain'].get())
        self.background_app.isRunning = False

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    launcher = MacropadLauncher()
    launcher.main()
from multiprocessing.context import Process
import time
import argparse
import sys
import os
import logging
import signal
from logging import handlers, debug
import multiprocessing
import setproctitle
from multiprocessing import Event, JoinableQueue

from app import MacroPadApp
from tray_icon_app import TrayIconApp
from macro_enums import InterProcessCommunication

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

    def restartBackgroundApp(event: Event, bg_proc_pid: int):
        debug("waiting for restarting event")
        event.wait()
        debug("now i should restart background process")
        os.kill(bg_proc_pid, signal.SIGTERM)
        # self.background_app.terminate()
        # self.background_app = MacroPadApp(vars(self.cmdargs), self.q)
        # self.background_app.start()

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

        self.q = JoinableQueue()

        restart_background_process_e = Event()

        self.background_app = MacroPadApp(vars(self.cmdargs), self.q)
        self.background_app.start()
        self.background_app_pid = self.background_app.pid

        restartBackgroundProcess = Process( name='restartbackground',
                                            target=MacropadLauncher.restartBackgroundApp,
                                            args=(restart_background_process_e,self.background_app_pid))
        restartBackgroundProcess.start()

        trayApp = TrayIconApp(self.q, 12, bg_restart_event=restart_background_process_e)
        trayApp.start()



        while not self.q.empty():
            debug(f"Result: {self.q.get()}")

        trayApp.join()
        while trayApp.is_alive():
            pass
        self.background_app.isRunning = False



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
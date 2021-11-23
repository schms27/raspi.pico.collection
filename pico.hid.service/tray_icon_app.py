import sys
from PyQt5.QtCore import QTimer
import setproctitle
from multiprocessing import Process
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu

from ui.main_window import MainConfigWindow
from macro_enums import InterProcessCommunication, ProcessState
from settings import Settings
import resources

WINDOW_TITLE = "MacroPad Configuration"
PROCESS_TITLE = "MacroPad-TrayIcon"

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        setproctitle.setproctitle(PROCESS_TITLE)
        menu = QMenu(parent)
        self.exit_action = menu.addAction("Quit")
        self.exit_action.triggered.connect(self.slot_exit)
        self.setContextMenu(menu)

    def slot_exit(self):
        QApplication.exit(0)

class TrayIconApp(Process):
    def __init__(self, arguments, queues, idx, **kwargs):
        super(TrayIconApp, self).__init__()
        self.queues = queues
        self.idx = idx
        self.kwargs = kwargs

        self.settings = Settings(arguments['settingspath'])
 
    def run(self):
        self.queues['toMain'].put((InterProcessCommunication.PROCESS_INFO, ProcessState.STARTED, self.idx, "Process idx={0} is started '{1}', kwargs: '{2}', sys.argv: '{3}".format(self.idx, self.name, self.kwargs, sys.argv), self.__class__.__name__))
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        app.setWindowIcon(QIcon(':/icons/makro_icon.ico'))

        self.window = MainConfigWindow(settings=self.settings, kwargs=self.kwargs, queues=self.queues)
        trayIcon = SystemTrayIcon(QIcon(':/icons/makro_icon.ico'), self.window)
        trayIcon.activated.connect(self.onTrayIconActivated)
        trayIcon.show()
        self.window.resize(1025, 800)
        self.window.move(300, 300)
        self.window.setWindowTitle(WINDOW_TITLE) 

        self.timer = QTimer()
        self.timer.timeout.connect(self.processQueueMessages)
        self.timer.start(1000)

        sys.exit(app.exec())

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.window.refreshUi()
            self.window.show()

    def processQueueMessages(self):
        if not self.queues['fromMain'].empty():
            response = self.queues['fromMain'].get()

            if(response[2] == self.__class__.__name__):
                self.queues['fromMain'].put(response)

            if response[0] == InterProcessCommunication.CHANGED_PASSWORD_SUCCESSFUL:
                wasSuccessful = response[1]
                self.window.setPasswordChangedSuccessful(wasSuccessful)

            
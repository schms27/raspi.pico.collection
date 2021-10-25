import sys
from multiprocessing import Process
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.exit_action = menu.addAction("Quit")
        self.exit_action.triggered.connect(self.slot_exit)
        self.setContextMenu(menu)

    def slot_exit(self):
        QApplication.exit(0)

class TrayIconApp(Process):
    def __init__(self, queue, idx, **kwargs):
        super(TrayIconApp, self).__init__()
        self.queue = queue
        self.idx = idx
        self.kwargs = kwargs

    def run(self):
        self.queue.put("Process idx={0} is called '{1}', kwargs: '{2}', sys.argv: '{3}".format(self.idx, self.name, self.kwargs, sys.argv))
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        app.setWindowIcon(QIcon("./dist/makro_icon.ico"))

        self.window = QWidget()
        trayIcon = SystemTrayIcon(QIcon("./dist/makro_icon.ico"), self.window)
        trayIcon.activated.connect(self.onTrayIconActivated)
        trayIcon.show()
        self.window.resize(250, 200)
        self.window.move(300, 300)

        self.window.setWindowTitle('Simple')

        sys.exit(app.exec())

    def onTrayIconActivated(self, reason):
        pass
        # self.window.show()
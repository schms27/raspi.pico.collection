from PyQt5.QtWidgets import QMainWindow, QLineEdit

from util import get_serial_ports

from ui.main_config_window import Ui_MainWindow

from macro_enums import InterProcessCommunication

class MainConfigWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, queue, parent=None, kwargs=None):
        super().__init__(parent)
        self.setupUi(self)

        self.queue = queue
        if 'bg_restart_event' in kwargs:
            self.restart_event = kwargs['bg_restart_event']

        self.com_port_comboBox.clear()
        self.com_port_comboBox.addItems(get_serial_ports())

        self.password_lineEdit.setEchoMode(QLineEdit.Password)

    def onSaveButtonClicked(self):
        pass
        
    def onResetButtonClicked(self):
        self.restart_event.set()
        # self.queue.put((InterProcessCommunication.RESTART_BACKGROUND_SERVICE, self.__class__.__name__))
        pass

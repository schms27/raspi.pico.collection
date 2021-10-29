from PyQt5.QtWidgets import QMainWindow, QLineEdit
from settings import Settings

from util import get_serial_ports, get_sound_device_names

from ui.main_config_window import Ui_MainWindow

from macro_enums import InterProcessCommunication

class MainConfigWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, queues, settings: Settings, parent=None, kwargs=None):
        super().__init__(parent)
        self.setupUi(self)

        self.queues = queues
        self.settings = settings
        self.com_port_comboBox.clear()
        self.com_port_comboBox.addItems(get_serial_ports())
        self.com_port_comboBox.setCurrentText(self.settings.getSetting('device_com_port'))

        self.sound_device_comboBox.clear()
        self.sound_device_comboBox.addItems(get_sound_device_names())
        self.sound_device_comboBox.setCurrentText(self.settings.getSetting('sound_playback_device'))

        self.password_lineEdit.setEchoMode(QLineEdit.Password)

    def onSaveButtonClicked(self):
        self.settings.setSetting('device_com_port', self.com_port_comboBox.currentText())
        self.settings.setSetting('sound_playback_device', self.sound_device_comboBox.currentText())
        self.settings.saveSettings()
        
    def onResetButtonClicked(self):
        self.queues['toMain'].put((InterProcessCommunication.RESTART_BACKGROUND_SERVICE, "", self.__class__.__name__))
        pass

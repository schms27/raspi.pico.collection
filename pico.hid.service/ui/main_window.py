import qtawesome as qta
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtCore import QSize
from settings import Settings

from util import get_serial_ports, get_sound_device_names

from ui.main_config_window import Ui_MainWindow

from macro_enums import InterProcessCommunication

class MainConfigWindow(QMainWindow, Ui_MainWindow):
    IconSize = QSize(24, 24)

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

        self.label_icon_password_set.setPixmap(qta.icon("fa5s.times-circle").pixmap(self.IconSize))

    def onSaveButtonClicked(self):
        self.settings.setSetting('device_com_port', self.com_port_comboBox.currentText())
        self.settings.setSetting('sound_playback_device', self.sound_device_comboBox.currentText())
        self.settings.saveSettings()

        if self.password_lineEdit.text():
            self.queues['fromMain'].put((InterProcessCommunication.CHANGED_PASSWORD, self.password_lineEdit.text(), self.__class__.__name__))
        
    def onResetButtonClicked(self):
        self.queues['toMain'].put((InterProcessCommunication.RESTART_BACKGROUND_SERVICE, "", self.__class__.__name__))
        pass

    def setPasswordChangedSuccessful(self, wasSuccessful: bool) -> None:
        if wasSuccessful:
            self.label_icon_password_set.setPixmap(qta.icon("fa5s.check-circle").pixmap(self.IconSize))
        else:
            self.label_icon_password_set.setPixmap(qta.icon("fa5s.times-circle").pixmap(self.IconSize))
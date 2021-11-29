import qtawesome as qta
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import QSize
from settings import Settings
from layout_manager import LayoutManager, SwapDirection
from functools import partial

from util import get_serial_ports, get_sound_device_names

from ui.main_config_window import Ui_MainWindow

from ui.button_function_dialog import ButtonFunctionDialog

from macro_enums import InterProcessCommunication, Color

class MainConfigWindow(QMainWindow, Ui_MainWindow):
    IconSize = QSize(24, 24)

    def __init__(self, queues, settings: Settings, parent=None, kwargs=None):
        super().__init__(parent)
        self.setupUi(self)

        self.queues = queues
        self.settings = settings
        self.layoutManager = LayoutManager(self.settings)

        self.refreshUi()

        self.password_lineEdit.setEchoMode(QLineEdit.Password)

        self.label_icon_password_set.setPixmap(qta.icon("fa5s.times-circle").pixmap(self.IconSize))

        self.lineEdit_layout_name.textChanged.connect(self.onLayoutNameChanged)
        

        for key in range(0, 16):
            pb = self.findChild(QPushButton, f"pushButton_f_{key}")
            pb.clicked.connect(partial(self.onFunctionButtonClicked, key))

    def onCurrentColorChanged(self, cb_index, value):
        if value:
            self.setButtonColor(cb_index, value)
            self.layoutManager.setBaseColor(cb_index, value)

    def onFunctionButtonClicked(self, btn_index):
        actions = self.layoutManager.getAction(btn_index)
        dlg = ButtonFunctionDialog(actions)
        if dlg.exec():
            # TODO: save dlg.functionDefinitions[dlg.currentFunctionDef] to LayoutManager
            print("Success!")
        else:
            print("Cancel!")

    def refreshUi(self):
        self.com_port_comboBox.clear()
        self.com_port_comboBox.addItems(get_serial_ports())
        self.com_port_comboBox.setCurrentText(self.settings.getSetting('device_com_port'))

        self.sound_device_comboBox.clear()
        self.sound_device_comboBox.addItems(get_sound_device_names())
        self.sound_device_comboBox.setCurrentText(self.settings.getSetting('sound_playback_device'))

        self.initColorDropdowns()

        self.loadLayout()


    def onSaveButtonClicked(self):
        self.settings.setSetting('device_com_port', self.com_port_comboBox.currentText())
        self.settings.setSetting('sound_playback_device', self.sound_device_comboBox.currentText())
        self.settings.saveSettings()

        self.layoutManager.saveLayout()

        if self.password_lineEdit.text():
            self.queues['fromMain'].put((InterProcessCommunication.CHANGED_PASSWORD, self.password_lineEdit.text(), self.__class__.__name__))
        
    def onResetButtonClicked(self):
        self.queues['toMain'].put((InterProcessCommunication.RESTART_BACKGROUND_SERVICE, "", self.__class__.__name__))

    def onNewLayoutButtonClicked(self):
        self.layoutManager.createNewLayout()
        self.onNextLayoutButtonClicked()

    def onDeleteLayoutButtonClicked(self):
        self.layoutManager.deleteCurrentLayout()
        self.loadLayout()

    def onNextLayoutButtonClicked(self):
        self.layoutManager.swapLayout(SwapDirection.FORWARD.name)
        self.loadLayout()

    def onPrevLayoutButtonClicked(self):
        self.layoutManager.swapLayout(SwapDirection.BACKWARD.name)
        self.loadLayout()

    def onLayoutNameChanged(self):
        self.layoutManager.setCurrentLayoutName(self.lineEdit_layout_name.text())

    def setPasswordChangedSuccessful(self, wasSuccessful: bool) -> None:
        if wasSuccessful:
            self.label_icon_password_set.setPixmap(qta.icon("fa5s.check-circle").pixmap(self.IconSize))
        else:
            self.label_icon_password_set.setPixmap(qta.icon("fa5s.times-circle").pixmap(self.IconSize))

    def initColorDropdowns(self):
        for key in range(0, 16):
            cb = self.findChild(QComboBox, f"comboBox_color_{key}")
            try:
                cb.currentTextChanged.disconnect()
            except:
                pass
            cb.clear()
            cb.addItems([e.name.lower() for e in Color])
            cb.currentTextChanged.connect(partial(self.onCurrentColorChanged, key))
            

    def setButtonColor(self, btn_index, color):
        button = self.findChild(QPushButton, f"pushButton_{btn_index}")
        button.setStyleSheet(f"background-color: {color}")

    def loadLayout(self):
        self.lineEdit_layout_name.setText(self.layoutManager.getCurrentLayoutName())
        keycolors = self.layoutManager.getBaseColors()
        for key, _ in enumerate(keycolors):
            color = keycolors[key].lower()
            self.setButtonColor(key, color)
            cb = self.findChild(QComboBox, f"comboBox_color_{key}")
            cb.setCurrentText(color)
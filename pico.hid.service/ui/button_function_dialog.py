from PyQt5.QtWidgets import QDialog

from ui._button_function_dialog import Ui_Dialog

from macro_enums import Order, Action

class ButtonFunctionDialog(QDialog, Ui_Dialog):
    def __init__(self, functionDefinitions: list, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.functionDefinitions = functionDefinitions
        self.currentFunctionDef = 0

        self.refreshUi()
        self.setWindowTitle("Edit Function Definition")

        self.comboBox_keycode.currentTextChanged.connect(self.onInputChanged)
        self.comboBox_actionType.currentTextChanged.connect(self.onInputChanged)


    def accept(self) -> None:
        return super().accept()

    def reject(self) -> None:
        return super().reject()

    def onInputChanged(self):
        self.functionDefinitions[self.currentFunctionDef]['keycode'] = self.comboBox_keycode.currentText()
        self.functionDefinitions[self.currentFunctionDef]['action']['type'] = self.comboBox_actionType.currentText()

    def refreshUi(self):
        self.lineEdit_keynumber.setText(str(self.functionDefinitions[self.currentFunctionDef]['key']))
        
        self.comboBox_keycode.clear()
        self.comboBox_keycode.addItems([o.name for o in Order])
        self.comboBox_keycode.setCurrentText(str(self.functionDefinitions[self.currentFunctionDef]['keycode']))
        
        self.comboBox_actionType.clear()
        self.comboBox_actionType.addItems([a.name for a in Action])
        self.comboBox_actionType.setCurrentText(str(self.functionDefinitions[self.currentFunctionDef]['action']['type']))
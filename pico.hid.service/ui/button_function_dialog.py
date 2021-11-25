from PyQt5.QtWidgets import QDialog

class ButtonFunctionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")
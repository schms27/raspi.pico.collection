import win32api
import win32gui
import win32con 
import win32com.client
from enum import Enum


class MixerCommand(Enum):
    MIC_MUTE = 0
    SOUND_MUTE = 1


class SoundMixer():
    def __init__(self):
        self.WM_APPCOMMAND = 0x319
        self.APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000

    def send_input_hax(self, hwnd, msg):
        for c in msg:
            if c == "\n":
                win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)

    def toggleMic(self):
        """
        https://stackoverflow.com/questions/50025927/how-mute-microphone-by-python
        """
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.AppActivate("Discord")
        shell.SendKeys("^m", 0)
        hwnd_active = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd_active, self.WM_APPCOMMAND, None, self.APPCOMMAND_MICROPHONE_VOLUME_MUTE)

    def execCommand(self, command):
        if command == MixerCommand.MIC_MUTE.name:
            self.toggleMic()
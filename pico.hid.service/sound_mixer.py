from subprocess import call
import win32api
import win32gui
import win32con 
import win32com.client
from enum import Enum
import sounddevice as sd
import soundfile as sf
import numpy as np


class MixerCommand(Enum):
    MIC_MUTE = 0
    SOUND_MUTE = 1
    PLAY_FILE = 2


class SoundMixer():
    def __init__(self):
        self.WM_APPCOMMAND = 0x319
        self.APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
        self.APPCOMMAND_SYSTEM_VOLUME_MUTE = 0x80000
        self.IsMuted = False
        self.IsSoundMuted = False
        # print(sd.query_devices())
        sd.default.device = next(x for x in sd.query_devices() if "CABLE Input (VB-Audio" in x['name'])['name']

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

    def toggleSystemSound(self):
        hwnd_active = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd_active, self.WM_APPCOMMAND, None, self.APPCOMMAND_SYSTEM_VOLUME_MUTE)
        pass

    def playFile(self, filepath):
        if filepath is not None:
            array, smp_rt = sf.read(filepath)
            try: 
                sd.play(array, smp_rt)
                sd.wait()
                sd.stop()
            except:
                return False
            return True

    def execCommand(self, action, callback=None):
        command = action['command']
        if command == MixerCommand.MIC_MUTE.name:
            self.toggleMic()
            self.IsMuted = not self.IsMuted
        elif command == MixerCommand.SOUND_MUTE.name:
            self.toggleSystemSound()
            self.IsSoundMuted = not self.IsSoundMuted
        elif command == MixerCommand.PLAY_FILE.name:
            filepath = action['filepath']
            print(f"Started to play file '{filepath}'")
            successful = self.playFile(filepath)
            print("Played file '{0}' successfully: {1}".format(filepath, successful))
        if callback is not None:
            callback()
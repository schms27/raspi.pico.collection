from subprocess import call
import win32api
import win32gui
import win32con 
import win32com.client
from enum import Enum
import sounddevice as sd
from scipy.io.wavfile import read
import requests
import json
import numpy as np


class MixerCommand(Enum):
    MIC_MUTE = 0
    SOUND_MUTE = 1
    PLAY_FILE = 2
    MUSIC_TOGGLE_PLAY = 3
    MUSIC_NEXT_TRACK = 4
    MUSIC_PREV_TRACK = 5
    MUSIC_TOGGLE_MUTE = 6

class MusicService(Enum):
    VOLUMIO_LOCAL = 0
    SPOTIFY = 1


class SoundMixer():
    def __init__(self, settings):
        self.WM_APPCOMMAND = 0x319
        self.APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
        self.APPCOMMAND_SYSTEM_VOLUME_MUTE = 0x80000
        self.IsMuted = False
        self.IsSoundMuted = False
        self.prev_volume = 20 # default 'not-muted' volume
        # print(sd.query_devices())
        playbackDevice = settings.getSetting("sound_playback_device")
        if playbackDevice != "default":
            sd.default.device = next(x for x in sd.query_devices() if playbackDevice in x['name'])['name']

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
            a = read(filepath)
            array = np.array(a[1], dtype=float)
            smp_rt = 44100
            try: 
                sd.play(array, smp_rt)
                sd.wait()
                sd.stop()
            except:
                return False
            return True

    def togglePlayMusic(self, service):
        if service == MusicService.VOLUMIO_LOCAL.name:
            r = requests.get("http://volumio.local/api/v1/commands/?cmd=toggle")
            if r.status_code != 200:
                print(f"failed to toggle music, reason: {r.reason}")
        else:
            print("Service not implemented")

    def playNextTrack(self, service):
        if service == MusicService.VOLUMIO_LOCAL.name:
            r = requests.get("http://volumio.local/api/v1/commands/?cmd=next")
            if r.status_code != 200:
                print(f"failed to skip to next track, reason: {r.reason}")
        else:
            print("Service not implemented")

    def playPreviousTrack(self, service):
        if service == MusicService.VOLUMIO_LOCAL.name:
            requests.get("http://volumio.local/api/v1/commands/?cmd=prev")
            r = requests.get("http://volumio.local/api/v1/commands/?cmd=prev")
            if r.status_code != 200:
                print(f"failed to skip to previous track, reason: {r.reason}")
        else:
            print("Service not implemented")

    def toggleMuteMusic(self, service):
        if service == MusicService.VOLUMIO_LOCAL.name:
            newVol = self.prev_volume
            currVol = self.getMusicServiceVolume(service)
            if currVol > 0:
                newVol = 0
            self.prev_volume = currVol
            r = requests.get(f"http://volumio.local/api/v1/commands/?cmd=volume&volume={newVol}")
            if r.status_code != 200:
                print(f"failed to toggle mute music, reason: {r.reason}")
        else:
            print("Service not implemented")

    def getMusicServiceVolume(self, service=MusicService.VOLUMIO_LOCAL.name):
        if service == MusicService.VOLUMIO_LOCAL.name:
            r = requests.get("http://volumio.local/api/v1/getState")        
            j_response = json.loads(r.content.decode())
            return j_response["volume"]

    def isMusicMuted(self):
        return False if self.getMusicServiceVolume() > 0 else True

    def isMusicPlaying(self, service=MusicService.VOLUMIO_LOCAL.name):
        if service == MusicService.VOLUMIO_LOCAL.name:
            r = requests.get("http://volumio.local/api/v1/getState")        
            j_response = json.loads(r.content.decode())
            return True if j_response["status"] == "play" else False

    def execCommand(self, action, callback=None):
        command = action['command']
        if command == MixerCommand.MIC_MUTE.name:
            self.toggleMic()
            self.IsMuted = not self.IsMuted
        elif command == MixerCommand.SOUND_MUTE.name:
            self.toggleSystemSound()
            self.IsSoundMuted = not self.IsSoundMuted
        elif command == MixerCommand.MUSIC_TOGGLE_PLAY.name:
            self.togglePlayMusic(action['service'])
        elif command == MixerCommand.MUSIC_TOGGLE_MUTE.name:
            self.toggleMuteMusic(action['service'])
        elif command == MixerCommand.MUSIC_NEXT_TRACK.name:
            self.playNextTrack(action['service'])
        elif command == MixerCommand.MUSIC_PREV_TRACK.name:
            self.playPreviousTrack(action['service'])
        elif command == MixerCommand.PLAY_FILE.name:
            filepath = action['filepath']
            print(f"Started to play file '{filepath}'")
            successful = self.playFile(filepath)
            print("Played file '{0}' successfully: {1}".format(filepath, successful))
        if callback is not None:
            callback()
import os
import time
import subprocess
import pyperclip
from serial import Serial, SerialException, PARITY_NONE, STOPBITS_ONE, EIGHTBITS

from macro_enums import Order, Action, Color
from settings import Settings
from keyboard_manager import KeyboardManager
from layout_manager import LayoutManager
from password_manager import PasswordManager
from sound_mixer import SoundMixer, MixerCommand
from program_executer import ProgramExecuter

class MacroPadApp():
    def __init__(self, arguments, log) -> None:
        self.isDeviceConnected = False
        self.isDeviceReady = False
        self.refreshRate = 0.5

        self.isRunningAsService = False

        self.settings = Settings(arguments.settingspath)
        self.passwordManager = PasswordManager(log, self.settings)
        self.layoutManager = LayoutManager(self.settings)
        self.keyboardManager = KeyboardManager()
        self.soundMixer = SoundMixer(log, self.settings)
        self.exec = ProgramExecuter()

        self.log = log

        if arguments.password is not None:
            self.passwordManager.prepare_passwordfile(arguments.password)

    def connect(self):
        serialPort = self.settings.getSetting('device_com_port')
        try:
            print(f"Connecting to port '{serialPort}...'")
            self.ser = Serial(
                port=serialPort, 
                baudrate=9600,
                parity=PARITY_NONE,
                stopbits=STOPBITS_ONE,
                bytesize=EIGHTBITS,
                timeout=1)
        except PermissionError as e:
            self.log(e.strerror)
            return
        except (SerialException, FileNotFoundError) as e:
            self.log(f"Cannot find device on Port '{serialPort}'")
            self.log(f"Error '{e}'")
        except Exception as e:
            print(e)
            raise e
        else:
            self.isDeviceConnected = True
            self.log(f"Successfully connected to device on port '{serialPort}'")
            return
        self.isDeviceConnected = False
        self.isDeviceReady = False

    def readSerial(self) -> None:
        try:
            bytestoread = self.ser.inWaiting()
            if bytestoread != 0:
                self.log(f"in waiting: {bytestoread}")
                serialData = self.ser.readline().strip()
                self.parseInput(serialData)
        except Exception as e:
            self.log(f"reading exception: {e}")
            self.isDeviceConnected = False
            self.connect()

    def run_program(self, path) -> None:
        if self.isRunningAsService:
            domainName = "desktop-kn035je" 
            userName = "simu"
            password = "c-mu1337" 
            maxWaitMs = 60000
            self.exec.runAsDomainUser(domainName, userName, password, path, maxWaitMs)
        else:
            subprocess.Popen(path)



    # ---------------- MOVE TO MESSAGE BUILDER CLASS ------------------
    def build_message(self, command, *args) -> str:
        message = self.get_hexdata(command)
        for arg in args:
            hexarg = self.get_hexdata(arg[0], arg[1])
            message += f" {hexarg}"
        return f"{message}\r"

    def get_hexdata(self, base10, padding=2) -> str:
        return "0x%0*X" % (padding,base10)

    def send_message(self, payload: str) -> None:
        self.ser.write(payload) 
        self.ser.flush()
        time.sleep(0.00)
    # ---------------- END: MOVE TO MESSAGE BUILDER CLASS ------------------

    # ---------------- MOVE TO COLOR? CLASS ------------------
    def set_color(self, key, color) -> None:
        reply = self.build_message(Order.SET_COLOR.value, (key, 2), (int(color, 0),6))
        self.send_message(bytes(reply, encoding='utf-8'))

    def set_multi_color(self, colorstrings) -> None:
        reply = self.build_message(Order.SET_MULTI_COLOR.value, *[(int(Color[colorstrings[i]].value, 0), 6) for i in colorstrings])
        self.send_message(bytes(reply, encoding='utf-8'))

    def set_blink_color(self, key, color, interval) -> None:
        reply = self.build_message(Order.SET_BLINK_COLOR.value, (key, 2), (int(color, 0),6), (interval,3))
        self.send_message(bytes(reply, encoding='utf-8'))

    def set_base_colors(self) -> None:
        keycolors = self.layoutManager.getBaseColors()
        self.set_multi_color(keycolors)
    # ---------------- END: MOVE TO COLOR? CLASS ------------------

    def exec_establish_connection(self, command):
        if command == Order.HELLO:
            reply = self.build_message(Order.SERVICE_READY.value)
            self.send_message(bytes(reply,encoding='utf-8'))
        elif command == Order.DEVICE_READY:
            self.isDeviceReady = True
            self.set_base_colors()
        
    def exec_command(self, command, payload):
        args = payload.split()  

        key = None
        if len(args) > 0:
            key = int(args[0], 16)
        action = self.layoutManager.getAction(command, key)
        if action == None or command == Order.HELLO or command == Order.DEVICE_READY:
            return
        if action['type'] == Action.RUN_PROGRAM.name:
            self.run_program(action['program'])
        elif action['type'] == Action.SWAP_LAYOUT.name:
            self.layoutManager.swapLayout(action['direction'])
            self.set_base_colors()
        elif action['type'] == Action.SOUND_MIXER.name:
            command = action['command']
            keycolors = self.layoutManager.getBaseColors()
            colorStr = keycolors[key]
            if command == MixerCommand.MIC_MUTE.name:
                colorStr = action['toggleColors']['onColor']
                if self.soundMixer.IsMuted:
                    colorStr = action['toggleColors']['offColor']
            elif command == MixerCommand.SOUND_MUTE.name:
                colorStr = action['toggleColors']['onColor']
                if self.soundMixer.IsSoundMuted:
                    colorStr = action['toggleColors']['offColor']
            elif command == MixerCommand.MUSIC_TOGGLE_PLAY.name:
                colorStr = action['toggleColors']['offColor']
                if self.soundMixer.isMusicPlaying():
                    colorStr = action['toggleColors']['onColor']
            elif command == MixerCommand.MUSIC_TOGGLE_MUTE.name:
                colorStr = action['toggleColors']['onColor']
                if self.soundMixer.isMusicMuted():
                    colorStr = action['toggleColors']['offColor']
            elif command == MixerCommand.PLAY_FILE.name:
                self.set_blink_color(key, Color[keycolors[key]].value, 150)
            self.soundMixer.execCommand(action, lambda: self.set_color(key, Color[colorStr].value))
        elif action['type'] == Action.PASTE_SENSITIVE_INFORMATION.name:
            sens_val = self.passwordManager.get_password(action['password_name'])
            pyperclip.copy(sens_val)
            self.keyboardManager.sendPaste()

    def parseCommand(self, command) -> Order:
        return Order(int(command, 0))

    def parseInput(self, rawData) -> None:
        data = rawData.decode('utf-8')
        self.log(data)
        if data[:2] == '0x':
            command = self.parseCommand(data[:4])
            if self.isDeviceReady:
                self.exec_command(command, data[4:])
            else:
                self.exec_establish_connection(command)

    def loop(self) -> None:
        if not self.isDeviceConnected:
            self.connect()
        else:
            self.readSerial()

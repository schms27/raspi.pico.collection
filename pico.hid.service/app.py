import sys
import time
import subprocess
import pyperclip
import setproctitle
from random import randint
from multiprocessing import Process
from serial import Serial, SerialException, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
from logging import debug, info, warning, error

from macro_enums import Order, Action, Color, InterProcessCommunication, ProcessState
from settings import Settings
from input_manager import InputManager
from layout_manager import LayoutManager
from password_manager import PasswordManager
from sound_mixer import SoundMixer, MixerCommand
from time_journal import TimeJournal
from util import calculateNextReconnectInterval

class MacroPadApp(Process):
    def __init__(self, arguments, queues, idx, **kwargs) -> None:
        super(MacroPadApp, self).__init__()
        setproctitle.setproctitle("MacroPad-Background")
        self.arguments = arguments
        self.queues = queues
        self.idx = idx
        self.kwargs = kwargs

        self.isDeviceConnected = False
        self.isDeviceReady = False
        self.reconnectInterval = 1
        self.reconnectCounter = 0
        self.cycleCounter = 0

        self.isRunning = True

        self.settings = Settings(self.arguments['settingspath'])

        self.passwordManager = PasswordManager(self.settings)
        self.layoutManager = LayoutManager(self.settings)
        self.inputManager = InputManager(self)
        self.soundMixer = SoundMixer(self.settings)
        self.timeJournal = TimeJournal(self.settings)

        if self.arguments["password"] is not None:
            self.passwordManager.prepare_passwordfile(self.arguments['password'])

    def run(self):
        self.soundMixer.setup_sound_device(self.settings.getSetting("sound_playback_device"))
        self.queues['toMain'].put((InterProcessCommunication.PROCESS_INFO, ProcessState.STARTED, self.idx,"Process idx={0} is started '{1}', kwargs: '{2}', sys.argv: '{3}".format(self.idx, self.name, self.kwargs, sys.argv), self.__class__.__name__))
        while self.isRunning:
            self.loop()
            self.processQueueMessages()
            time.sleep(0.1)

    def connect(self):
        if self.cycleCounter % int(round(self.reconnectInterval)) != 0:
            return
        serialPort = self.settings.getSetting('device_com_port')
        self.reconnectCounter += 1
        try:
            info(f"Connecting to port '{serialPort}', reconnecting for the '{self.reconnectCounter}' time")
            self.ser = Serial(
                port=serialPort, 
                baudrate=9600,
                parity=PARITY_NONE,
                stopbits=STOPBITS_ONE,
                bytesize=EIGHTBITS,
                timeout=1)
        except PermissionError as e:
            warning(e.strerror)
            return
        except (SerialException, FileNotFoundError) as e:
            warning(f"Cannot find device on Port '{serialPort}'")
            debug(f"Error '{e}'")
        except Exception as e:
            error(e)
            raise e
        else:
            self.isDeviceConnected = True
            self.reconnectCounter = 0
            self.reconnectInterval = 1
            info(f"Successfully connected to device on port '{serialPort}'")
            return
        self.reconnectInterval = calculateNextReconnectInterval(self.reconnectCounter, self.reconnectInterval)
        self.isDeviceConnected = False
        self.isDeviceReady = False
        self.cycleCounter = 0

    def processQueueMessages(self):
        if not self.queues['fromMain'].empty():
            response = self.queues['fromMain'].get()

            if(response[2] == self.__class__.__name__):
                self.queues['fromMain'].put(response)
                time.sleep(randint(1,5))

            if response[0] == InterProcessCommunication.REQUEST_RESTART_MACROPAD:
                self.sendRestartRequest()
            elif response[0] == InterProcessCommunication.CHANGED_PASSWORD:
                successful = self.passwordManager.prepare_passwordfile(response[1])
                self.queues['fromMain'].put((InterProcessCommunication.CHANGED_PASSWORD_SUCCESSFUL, successful, self.__class__.__name__))

    def readSerial(self) -> None:
        try:
            bytestoread = self.ser.inWaiting()
            if bytestoread != 0:
                debug(f"in waiting: {bytestoread}")
                serialData = self.ser.readline().strip()
                self.parseInput(serialData)
        except Exception as e:
            warning(f"reading exception: {e}")
            self.isDeviceConnected = False
            self.connect()

    def run_program(self, path) -> None:
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
        if self.isDeviceConnected:
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

    def sendRestartRequest(self):
        reply = self.build_message(Order.RESTART_BOARD.value)
        self.send_message(bytes(reply, encoding='utf-8'))

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
        action = self.layoutManager.getAction(key, command)
        if not action or command == Order.HELLO or command == Order.DEVICE_READY:
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
            password_key = action['password_name']
            sens_val = self.passwordManager.get_password(password_key)
            if sens_val is None:
                warning(f"Sensitive Information with name '{password_key}' not found")
                return
            pyperclip.copy(sens_val)
            self.inputManager.sendPaste()
        elif action['type'] == Action.INPUT.name:
            self.inputManager.execCommand(action, key)
        elif action['type'] == Action.TIME_JOURNAL.name:
            self.timeJournal.execCommand(action, key)
            

    def parseCommand(self, command) -> Order:
        return Order(int(command, 0))

    def parseInput(self, rawData) -> None:
        data = rawData.decode('utf-8')
        debug(data)
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
        self.cycleCounter += 1
        self.inputManager.loop()

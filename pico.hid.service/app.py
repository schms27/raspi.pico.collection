import os
import time
from serial import Serial, SerialException, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
from password_manager import PasswordManager
from settings import Settings


class MacroPadApp():
    def __init__(self, arguments, log) -> None:
        self.isDeviceConnected = False
        self.isDeviceReady = False
        self.refreshRate = 0.5

        self.passwordManager = PasswordManager()
        self.settings = Settings(arguments.settingspath)

        self.log = log

        if arguments.password is not None:
            pw = arguments.password

            passwordpath = self.settings.getSetting('password_filepath')
            passwordfile_clear = "passwords.json"
            passwordfile_enc = "passwords.encrypted"
            if not os.path.isfile(os.path.join(passwordpath, passwordfile_enc)):
                self.log( "Set Password to encrypt passwordfile (must be named 'passwords.json'):")
                self.passwordManager.encrypt_file(os.path.join(passwordpath, passwordfile_clear), pw)

            self.log( "Decrypt passwordfile")
            self.passwordManager.decrypt_file(os.path.join(passwordpath,passwordfile_enc), pw)

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
            self.isDeviceConnected = True
            time.sleep(3)
        except PermissionError as e:
            print(e.strerror)
            raise Exception
        except (SerialException, FileNotFoundError) as e:
            self.log(f"Cannot find device on Port '{serialPort}'")
            raise Exception
        except Exception as e:
            print(e)
            self.isDeviceConnected = False
            self.isDeviceReady = False
            return
        self.log(f"Successfully connected to device on port '{serialPort}'")

    def readSerial(self) -> None:
        try:
            bytestoread = self.ser.inWaiting()
            if bytestoread != 0:
                serialData = self.ser.readline().strip()
                self.parseInput(serialData)
        except:
            self.isDeviceConnected = False
            self.connect()

    def parseInput(self, serialData) -> None:
        print(serialData)
        pass

    def loop(self) -> None:
        if not self.isDeviceConnected:
            self.connect()
        else:
            self.readSerial()
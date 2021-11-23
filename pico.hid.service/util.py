import os
import sys
import glob
import serial
import sounddevice as sd
from numpy import log as ln
from logging import debug

fibonacci = lambda n:pow(2<<n,n+1,(4<<2*n)-(2<<n)-1)%(2<<n)


# Function to find the `k` closest elements to `target` in a sorted integer array `nums`
def findKClosestElements(nums, k, target):
 
    left = 0
    right = len(nums) - 1
 
    while right - left >= k:
        if abs(nums[left] - target) > abs(nums[right] - target):
            left = left + 1
        else:
            right = right - 1
 
    return nums[left:left + k]

def calculateNextReconnectInterval(counter: int, currentInterval: float) -> float:
    return max(currentInterval + ln(counter), currentInterval)

def resolvePath(pathRaw: str) -> str:
    variable = pathRaw.split('<',1)[-1].split('>',1)[0]
    if variable != pathRaw:
        expandedVar = os.getenv(variable)
        if expandedVar is not None:
            return pathRaw.replace(f"<{variable}>", expandedVar)
    return pathRaw

def get_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException) as e:
            if "Access is denied" in e.args[0]:
                result.append(port)
            else:
                debug(f"Port not accessible: {e}")
            continue
    return result

def get_sound_device_names(hostapi = 0):
    soundDevicesNames = ["default"]
    for dev in sd.query_devices():
        if dev['hostapi'] == hostapi:
            soundDevicesNames.append(dev['name'])
    return soundDevicesNames
import time
import board
import array
from pulseio import PulseIn, PulseOut

# https://techdocs.altium.com/display/FPGA/NEC+Infrared+Transmission+Protocol
ir_read = PulseIn(board.GP18, maxlen=100, idle_state=True)
ir_send = PulseOut(board.GP16, frequency=38000, duty_cycle=32768)

def betweenFuzzy(inVal, boundVal, lowerFactor=0.75, upperFactor=1.25):
    return boundVal * lowerFactor <= inVal <= boundVal * upperFactor

def parseIRValues(pulseArray):
    start = 9000
    startPause = 4500
    zeroLength = 563
    oneLength = 1688
    if len(pulseArray) < 10:
        return ""
        
    if betweenFuzzy(pulseArray[0], start) and betweenFuzzy(pulseArray[1], startPause):
        loopIndex = 0
        bin_str = ""
        for nextVal in pulseArray[2:]:
            if loopIndex % 2 == 0:
                loopIndex += 1
                continue
            if betweenFuzzy(nextVal, zeroLength):
                bin_str += "0"
            elif betweenFuzzy(nextVal, oneLength):
                bin_str += "1"
            loopIndex += 1
            
        print("binary code: ", bin_str)
        print("hex code: ", hex(int(bin_str, 2)))
    else:
        print("startcode invalid")

while True:
    read_vals = len(ir_read)
    print("read values: ", read_vals)
    if read_vals > 0:
        received_command = array.array('H', [ir_read[x] for x in range(len(ir_read)) if ir_read[x] < 15000])
        print("first value: ", received_command[0])
        print(received_command)
        parseIRValues(received_command)
        ir_read.clear()
    time.sleep(1)
import time
import board
import array
from pulseio import PulseIn, PulseOut

# https://techdocs.altium.com/display/FPGA/NEC+Infrared+Transmission+Protocol
ir_read = PulseIn(board.GP18, maxlen=100, idle_state=True)
ir_send = PulseOut(board.GP16, frequency=38000, duty_cycle=32768)

START_LEN = 9000
START_PAUSE_LEN = 4500
END_LEN = 9000
END_PAUSE_LEN = 2250
ZERO_LEN = 550
ONE_LEN = 1650

led_strip_commands = {
    "ON":           0x1ef807e,
    "OFF":          0x1ee817e,
    "MOD_UP":       0x1ee01fe,
    "MOD_DOWN":     0xf7807f,
    "RED":          0x1ee41be,
    "GREEN":        0x1ef40be,
    "BLUE":         0x1eec13e,
    "WHITE":        0x1efc03e,
    "ORANGE":       0x1ee21de,
    "LIGHT_GREEN":  0x1ef20de,
    "SKY_BLUE":     0x1eea15e,
    "LIGHT_ORANGE": 0x1ee619e,
    "LIGHT_BLUE":   0x1ef609e,
    "DARK_VIOLET":  0x1eee11e,
    "DARK_YELLOW":  0x1ee11ee,
    "INDIGO":       0x1ef10ee,
    "VIOLET":       0x1ee916e,
    "YELLOW":       0x1ee51ae,
    "DARK_INDIGO":  0x1ef50ae,
    "PINK":         0x1eed12e,
    "MOD_FLASH":    0x1efa05e,
    "MOD_STROBE":   0x1efe01e,
    "MOD_FADE":     0x1ef906e,
    "MOD_SMOOTH":   0x1efd02e
}

def betweenFuzzy(inVal, boundVal, lowerFactor=0.75, upperFactor=1.25):
    return boundVal * lowerFactor <= inVal <= boundVal * upperFactor

def convertHexToPulsearray(hexcode):
    binarystr = f'{hexcode:0>33b}' #bin(hexcode)
    print(f"hexcode: {hex(hexcode)}")
    print(f"binstr: {binarystr}")
    pulseArray = [START_LEN, START_PAUSE_LEN, ZERO_LEN]
    for c in binarystr[:-1]:
        if c == '0':
            pulseArray.append(ZERO_LEN)
        elif c == '1':
            pulseArray.append(ONE_LEN)
        else:
            raise Exception('Invalid char in binarystr')
        pulseArray.append(ZERO_LEN)

    pulseArray.append(END_LEN)
    pulseArray.append(END_PAUSE_LEN)
    pulseArray.append(ZERO_LEN)
    return array.array('H', pulseArray)
        
def parseIRValues(pulseArray):
    if len(pulseArray) < 10:
        return ""
        
    if betweenFuzzy(pulseArray[0], START_LEN) and betweenFuzzy(pulseArray[1], START_PAUSE_LEN):
        loopIndex = 0
        bin_str = ""
        for nextVal in pulseArray[2:]:
            if loopIndex % 2 == 0:
                loopIndex += 1
                continue
            if betweenFuzzy(nextVal, ZERO_LEN):
                bin_str += "0"
            elif betweenFuzzy(nextVal, ONE_LEN):
                bin_str += "1"
            loopIndex += 1
            
        print("binary code: ", bin_str)
        print("hex code: ", hex(int(bin_str, 2)))
    else:
        print("startcode invalid")

def readAndPrintIRInput():
    read_vals = len(ir_read)
    # print("read values: ", read_vals)
    if read_vals > 0:
        received_command = array.array('H', [ir_read[x] for x in range(len(ir_read)) if ir_read[x] < 15000])
        print("first value: ", received_command[0])
        print(received_command)
        parseIRValues(received_command)
        ir_read.clear()
    time.sleep(1) 

while True:
    # readAndPrintIRInput()
    print("start, turning on")
    arr = convertHexToPulsearray(led_strip_commands["ON"])
    print(f"array {arr}")
    ir_send.send(arr)

    for command in led_strip_commands:
        if command == "ON" or command == "OFF" or command == "OFF" or command == "OFF":
            continue
        hexCommand = led_strip_commands[command]
        print(f"setting command: '{command}, hexcode: {hex(hexCommand)}'")
        ir_send.send(convertHexToPulsearray(hexCommand))
        time.sleep(3)

    print("finished, turning off")
    ir_send.send(convertHexToPulsearray(led_strip_commands["OFF"]))
    time.sleep(30)
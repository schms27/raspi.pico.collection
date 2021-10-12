import time
import board
from analogio import AnalogIn


analog_in = AnalogIn(board.A2) # Analog pin on Seeedino XIAO

 
def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    print("Voltage: ", get_voltage(analog_in))
    time.sleep(1)
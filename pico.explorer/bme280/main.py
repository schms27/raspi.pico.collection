from breakout_bme680 import BreakoutBME680
from pimoroni_i2c import PimoroniI2C
import utime

PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

i2c = PimoroniI2C(**PINS_PICO_EXPLORER)
bme = BreakoutBME280(i2c)


while True:
    temperature, pressure, humidity = bme.read()
    print("Temperature: {0}° C, Pressure: {1} mBar, Humidity: {2}%".format(temperature, pressure, humidity))
    utime.sleep(5)    
    
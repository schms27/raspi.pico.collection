# This example takes the temperature from the Pico's onboard temperature sensor, and displays it on Pico Explorer, along with a little pixelly graph.
# It's based on the thermometer example in the "Getting Started with MicroPython on the Raspberry Pi Pico" book, which is a great read if you're a beginner!

from machine import Pin
import utime

# Pico Explorer boilerplate
import picoexplorer as display
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)





while True:
    if display.is_pressed(display.BUTTON_A):
        for i in range(0, 29):
            digital_pin = Pin(i, Pin.IN, Pin.PULL_DOWN)
            print("read value pin {0}: {1}".format(i, digital_pin.value()))
        break
        utime.sleep(10)   


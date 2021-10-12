# This example shows you a simple, non-interrupt way of reading Pico Explorer's buttons with a loop that checks to see if buttons are pressed.

import picoexplorer as display
import utime
from machine import Pin, ADC

# Initialise display with a bytearray display buffer
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(0, 0, 0)
    display.clear()
    display.update()

# unfortunately we cannot work with the built-in buttons because they are already blocked by
# the picoexplorer-library implementation (i guess at least), so here is an example with GPIO 0 - 3
# connect wire from 3v to the respective gpio to test the interrupt
button_a = Pin(0, Pin.IN, Pin.PULL_DOWN)
button_b = Pin(1, Pin.IN, Pin.PULL_DOWN)
button_x = Pin(2, Pin.IN, Pin.PULL_DOWN)
button_y = Pin(3, Pin.IN, Pin.PULL_DOWN)

def button_a_callback(pin):
    clear()                                           # clear to black
    display.set_pen(255, 255, 255)                    # change the pen colour
    display.text("Button A pressed", 10, 10, 240, 4)  # display some text on the screen
    display.update()                                  # update the display
    utime.sleep(1)                                    # pause for a sec
    clear()
    
def button_b_callback(pin):
    clear()                                           # clear to black
    display.set_pen(255, 255, 255)                    # change the pen colour
    display.text("Button B pressed", 10, 10, 240, 4)  # display some text on the screen
    display.update()                                  # update the display
    utime.sleep(1)                                    # pause for a sec
    clear()
    
def button_x_callback(pin):
    clear()                                           # clear to black
    display.set_pen(255, 255, 255)                    # change the pen colour
    display.text("Button X pressed", 10, 10, 240, 4)  # display some text on the screen
    display.update()                                  # update the display
    utime.sleep(1)                                    # pause for a sec
    clear()

def button_y_callback(pin):
    clear()                                           # clear to black
    display.set_pen(255, 255, 255)                    # change the pen colour
    display.text("Button Y pressed", 10, 10, 240, 4)  # display some text on the screen
    display.update()                                  # update the display
    utime.sleep(1)                                    # pause for a sec
    clear()   

button_a.irq(button_a_callback, Pin.IRQ_RISING)
button_b.irq(button_b_callback, Pin.IRQ_RISING)
button_x.irq(button_x_callback, Pin.IRQ_RISING)
button_y.irq(button_y_callback, Pin.IRQ_RISING)


    

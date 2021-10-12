# color_setup.py Customise for your hardware config

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021 Peter Hinch

# As written, supports:
# Adafruit 1.3" and 1.54" 240x240 Wide Angle TFT LCD Display with MicroSD - ST7789
# https://www.adafruit.com/product/4313
# https://www.adafruit.com/product/3787

# Demo of initialisation procedure designed to minimise risk of memory fail
# when instantiating the frame buffer. The aim is to do this as early as
# possible before importing other modules.

# WIRING (Adafruit pin nos and names).
# Pico  SSD
# VBUS  Vin
# Gnd   Gnd
# 8     D/C
# 9     TCS
# 15    RST
# 10    SCK
# 11    SI MOSI


# the example code is from https://github.com/peterhinch/micropython-nano-gui

from machine import Pin, SPI
import gc

from st7789 import *
SSD = ST7789

pdc = Pin(8, Pin.OUT, value=0)  # Arbitrary pins
pcs = Pin(9, Pin.OUT, value=1)
prst = Pin(15, Pin.OUT, value=1)
pbl = Pin(13, Pin.OUT, value=1)

gc.collect()  # Precaution before instantiating framebuf
# Conservative low baudrate. Can go to 62.5MHz. Depending on wiring.
spi = SPI(1, 30_000_000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
ssd = SSD(spi, dc=pdc, cs=pcs, rst=prst)

ssd.rect(70, 0, 50, 50, 0xFFFF)
ssd.fill_rect(0, 0, 50, 50, 0xFFFF)
ssd.text('Waveshare Test!', 0, 80, 0xFFFF)
ssd.hline(0, 90, 240, 0xFFFF)
ssd.vline(60, 90, 70, 0xFFFF)
ssd.show()

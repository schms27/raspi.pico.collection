from machine import Pin, I2C

# create an i2c object
i2c = I2C(0, scl=Pin(21), sda=Pin(20))

# Print out any addresses found
devices = i2c.scan()

if devices:
    for d in devices:
        print(hex(d))
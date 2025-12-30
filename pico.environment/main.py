# I2C Scanner MicroPython
from machine import Pin, SoftI2C
from time import sleep

# You can choose any other combination of I2C pins
i2c = SoftI2C(scl=Pin(7), sda=Pin(6))
device_addr=0x22

print('I2C SCANNER')
devices = i2c.scan()

def get_device_address():
    rbuf = i2c.readfrom_mem(device_addr, 0x04, 2)
    return rbuf[0] << 8 | rbuf[1]

def get_temperature():
    rbuf = i2c.readfrom_mem(device_addr, 0x14, 2)
    data = rbuf[0] << 8 | rbuf[1]
    temp = (-45) +((data * 175.00) / 1024.00 / 64.00)
    return round(temp, 2)

def get_humidity():
    rbuf = i2c.readfrom_mem(device_addr, 0x16, 2)
    data = rbuf[0] << 8 | rbuf[1]
    humidity = (data / 1024) * 100 / 64
    return round(humidity, 2)

def get_ultraviolet_intensity():
    rbuf = i2c.readfrom_mem(device_addr, 0x10, 2)
    data = rbuf[0] << 8 | rbuf[1]
    outputVoltage = 3000.0 * data/1024
    na =  (outputVoltage * 1000000000.0) / 4303300
    ultraviolet = na / 113
    return round(ultraviolet, 2)

def get_luminosity():
    rbuf = i2c.readfrom_mem(device_addr, 0x12, 2)
    data = rbuf[0] << 8 | rbuf[1]
    luminous = data * (1.0023 + data * (8.1488e-5 + data * (-9.3924e-9 + data * 6.0135e-13)))
    return round(luminous, 2)

def get_atmos_pressure():
    rbuf = i2c.readfrom_mem(device_addr, 0x18, 2)
    data = rbuf[0] << 8 | rbuf[1]
    pressure = data / 10
    return round(pressure, 2)

def get_elevation():
    rbuf = i2c.readfrom_mem(device_addr, 0x18, 2)
    data = rbuf[0] << 8 | rbuf[1]
    elevation = 44330 * (1.0 - pow(data / 1015.0, 0.1903));
    return round(elevation, 2)

addr = get_device_address()
print(f"Device Address: {addr}")
print("running....")

counter = 1
while True:
    print(f"_____MEASUREMENT NR: {counter}______")
    temperature = get_temperature()
    print(f"Temperature: \t\t\t{temperature} C°")
    rel_hum = get_humidity()
    print(f"Rel. Humidity: \t\t\t{rel_hum} %")
    ultraviolet = get_ultraviolet_intensity()
    print(f"Ultraviolet Intensity: \t\t{ultraviolet} lum")
    luminous = get_luminosity()
    print(f"Ambient Light: \t\t\t{luminous} lum")
    pressure = get_atmos_pressure()
    print(f"Atmospheric Pressure: \t\t{pressure} kPa")
    elevation = get_elevation()
    print(f"Elevation: \t\t\t{elevation} m")
    print("____________________________________\n")
    counter = counter + 1
    sleep(5)

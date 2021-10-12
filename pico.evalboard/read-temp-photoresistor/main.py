from machine import Pin, ADC 
import utime

#Initialize the ADC channel
photo_pin= ADC(Pin(26))      # Photoresistor Pin
sensor_temp = ADC(4)    # Internal Temperature Sensor Pin

while True:

    #Read ADC channel 0 voltage (Photoresistor)
    photo_volts = photo_pin.read_u16()*3.3/65535
    print("Photoresistor voltage = {0:.2f}V \r\n".format(photo_volts))
    print("Rel. Brightness = {0:.2f}% \r\n".format((photo_volts/3.3)*100))
    
    #Temperature is captured using an internal temperature sensor
    reading = sensor_temp.read_u16()*3.3/65535
    temperature = 27 - (reading - 0.706)/0.001721
    print("temperature = {0:.2f}℃ \r\n".format(temperature))
    
    utime.sleep_ms(1000)

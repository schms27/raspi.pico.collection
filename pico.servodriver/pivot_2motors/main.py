import time
from machine import Pin, PWM

# Construct PWM object, with LED on Pin(25).
tilt = PWM(Pin(3))
pan = PWM(Pin(4))

# Set the PWM frequency.
tilt.freq(50) # 20ms
pan.freq(50) # 20ms

speed = 200

# duty_u16 max 65535
tilt.duty_u16(4800)
pan.duty_u16(0)

for x in range(1):
    print("time: ", x+1)
    for i in range(4800,8200,speed):  
      tilt.duty_u16(i)
      time.sleep(0.01)
      
    for i in range(0,8200,speed):  
      pan.duty_u16(i)
      time.sleep(0.01)
      
    for i in range(8200,0,-speed):  
      pan.duty_u16(i)
      time.sleep(0.01)
    
    for i in range(8200,4800,-speed):
      tilt.duty_u16(i)
      time.sleep(0.01)
print("PWM down")
tilt.duty_u16(0)





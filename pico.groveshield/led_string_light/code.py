import board
import pwmio
import time
import digitalio

#led = digitalio.DigitalInOut(board.GP18)
#led.direction = digitalio.Direction.OUTPUT
#dac = analogio.AnalogOut(board.A2)   
led = pwmio.PWMOut(board.GP18, frequency=5000, duty_cycle=0)

# while True:
#     led.value = True
#     time.sleep(2.5)
#     led.value = False
#     time.sleep(2.5)7

duty = 0
while True:
    for i in range(100):
        # PWM LED up and down

        if i < 50:
            duty = int(i * 2 * 65535 / 100)
            led.duty_cycle =  duty # Up
        else:
            duty = 65535 - int((i - 50) * 2 * 65535 / 100)
            led.duty_cycle = duty # Down
        print(duty)
        time.sleep(0.1)
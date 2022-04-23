"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
from adafruit_motor import servo

# servo = pulseio.PWMOut(board.GP18,frequency=50,duty_cycle=2.5)
# servo.duty_cycle = 1.5

# create PWMOut objects
pwm = pwmio.PWMOut(board.GP16, duty_cycle=2 ** 15, frequency=50)
pwm2 = pwmio.PWMOut(board.GP17, duty_cycle=2 ** 15, frequency=50)

# Create servo objects
servo_1 = servo.Servo(pwm)
servo_2 = servo.Servo(pwm2)
counter = 0
while counter < 3:
    for angle in range(0, 180, 1):  # 0 - 180 degrees, 5 degrees at a time.
        #servo_1.angle = angle
        servo_2.angle = angle
        time.sleep(0.01)
    for angle in range(180, 0, -1): # 180 - 0 degrees, 5 degrees at a time.
        #servo_1.angle = angle
        servo_2.angle = angle
        time.sleep(0.01)
    counter += 1
"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
import digitalio
from adafruit_motor import servo

# servo = pulseio.PWMOut(board.GP18,frequency=50,duty_cycle=2.5)
# servo.duty_cycle = 1.5
switch = digitalio.DigitalInOut(board.GP27)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

# create PWMOut objects
pwm = pwmio.PWMOut(board.GP14, duty_cycle=2**13, frequency=50)
pwm2 = pwmio.PWMOut(board.GP12, duty_cycle=2**13, frequency=50)

# Create servo objects
servo_1 = servo.Servo(pwm)
servo_2 = servo.Servo(pwm2)

servo_1.angle = 0
servo_2.angle = 0
# time.sleep(0.5)

# servo_1.angle = 10
# servo_2.angle = 10

# time.sleep(0.5)

# servo_1.angle = 20
# servo_2.angle = 20

counter = 0
while True:
    if switch.value:
        for angle in range(0, 180, 1):  # 0 - 180 degrees, 5 degrees at a time.
            servo_2.angle = angle
            time.sleep(0.007)
        time.sleep(1)
        for angle in range(180, 0, -1): # 180 - 0 degrees, 5 degrees at a time.
            servo_2.angle = angle
            time.sleep(0.007)
        time.sleep(1)
        for angle in range(0, 180, 1):  # 0 - 180 degrees, 5 degrees at a time.
            servo_1.angle = angle
            time.sleep(0.007)
        time.sleep(1)
        for angle in range(180, 0, -1): # 180 - 0 degrees, 5 degrees at a time.
            servo_1.angle = angle
            time.sleep(0.007)
        counter += 1

servo_1.angle = 0
servo_2.angle = 0
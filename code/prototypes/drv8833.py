# Paul Schakel
# Prototype code for the DRV8833 H-Bridge board from Adafruit

from adafruit_motor import motor
import board
import pwmio
import time

A1 = board.GP10
A2 = board.GP11
pwmA1 = pwmio.PWMOut(A1, frequency=50)
pwmA2 = pwmio.PWMOut(A2, frequency=50)
motor1 = motor.DCMotor(pwmA1, pwmA2)
motor1.SLOW_DECAY

while True:
    motor1.throttle = 0.5
    time.sleep(5)
    motor1.throttle = 0
    time.sleep(2)
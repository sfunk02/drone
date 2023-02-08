# Paul Schakel
# Prototype for the TB6612FNG H-Bridge -- works better than DRV8833

import board
import pwmio
import digitalio

A1 = board.GP10
A2 = board.GP11
PWMA = board.GP13
motor1_pin1 = digitalio.DigitalInOut(A1)
motor1_pin1.direction = digitalio.Direction.OUTPUT
motor1_pin2 = digitalio.DigitalInOut(A2)
motor1_pin2.direction = digitalio.Direction.OUTPUT
motor1_pwm = pwmio.PWMOut(PWMA, frequency=1000)

while True:
    motor1_pin1.pull = digitalio.Pull.UP
    motor1_pin2.pull = digitalio.Pull.DOWN
    motor1_pwm.duty_cycle = 65535 // 2  # Cycles the pin with 50% duty cycle (half of 2 ** 16) at 50hz
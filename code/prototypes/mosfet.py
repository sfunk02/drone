# Paul Schakel
# Prototype for the mosfet

import board
import pwmio

MOTOR_1 = board.GP10
motor1_pwm = pwmio.PWMOut(MOTOR_1, frequency=1000)

while True:
    print("running")
    motor1_pwm.duty_cycle = 65535 // 2  # Cycles the pin with 50% duty cycle (half of 2 ** 16) at 50hz
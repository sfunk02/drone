# Paul Schakel
# Code for the first version of the drone project -- uses DRV8833 to drive motors

from adafruit_motor import motor
import board
import busio
import adafruit_mpu6050
import pwmio
import time 

PWM_FREQ = 125
DECAY_MODE = motor.FAST_DECAY

A1 = board.GP10
A2 = board.GP11
B1 = board.GP12
B2 = board.GP13
C1 = board.GP18
C2 = board.GP19
D1 = board.GP20
D2 = board.GP21
pwmA1 = pwmio.PWMOut(A1, frequency=PWM_FREQ)
pwmA2 = pwmio.PWMOut(A2, frequency=PWM_FREQ)
motor1 = motor.DCMotor(pwmA1, pwmA2)
motor1.decay_mode = (DECAY_MODE)
pwmB1 = pwmio.PWMOut(B1, frequency=PWM_FREQ)
pwmB2 = pwmio.PWMOut(B2, frequency=PWM_FREQ)
motor2 = motor.DCMotor(pwmB1, pwmB2)
motor2.decay_mode = (DECAY_MODE)
pwmC1 = pwmio.PWMOut(C1, frequency=PWM_FREQ)
pwmC2 = pwmio.PWMOut(C2, frequency=PWM_FREQ)
motor3 = motor.DCMotor(pwmC1, pwmC2)
motor3.decay_mode = (DECAY_MODE)
pwmD1 = pwmio.PWMOut(D1, frequency=PWM_FREQ)
pwmD2 = pwmio.PWMOut(D2, frequency=PWM_FREQ)
motor4 = motor.DCMotor(pwmD1, pwmD2)
motor4.decay_mode = (DECAY_MODE)

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

throttle_speed = 1

while True:
    motor1.throttle = throttle_speed
    motor2.throttle = throttle_speed
    motor3.throttle = -throttle_speed
    motor4.throttle = -throttle_speed
    print(throttle_speed)

    time.sleep(0.2)
    print(f"x: {round(mpu.acceleration[0], 3)} y: {round(mpu.acceleration[1], 3)} z: {round(mpu.acceleration[2], 3)}")
    motor1.throttle = mpu.acceleration[1] / 10.0
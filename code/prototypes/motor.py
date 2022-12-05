from adafruit_motor import motor
import board
import busio
import adafruit_mpu6050
import pwmio
import time

A1 = board.GP14
A2 = board.GP15
pwmA1 = pwmio.PWMOut(A1, frequency=50)
pwmA2 = pwmio.PWMOut(A2, frequency=50)
motor1 = motor.DCMotor(pwmA1, pwmA2)
B1 = board.GP12
B2 = board.GP13
pwmB1 = pwmio.PWMOut(B1, frequency=50)
pwmB2 = pwmio.PWMOut(B2, frequency=50)
motor2 = motor.DCMotor(pwmB1, pwmB2)

sda_pin = board.GP16
scl_pin = board.GP17
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

while True:
    # motor1.throttle = 1
    # print(motor1.throttle)
    # time.sleep(2)
    # motor1.throttle = 0
    # print(motor1.throttle)
    # time.sleep(2)
    # motor1.throttle = -1
    # print(motor1.throttle)
    # time.sleep(2)
    # motor1.throttle = 0
    # print(motor1.throttle)
    # time.sleep(20)

    time.sleep(0.2)
    print(f"x: {round(mpu.acceleration[0], 3)} y: {round(mpu.acceleration[1], 3)} z: {round(mpu.acceleration[2], 3)}")
    motor1.throttle = mpu.acceleration[1] / 10.0
    print(motor1.throttle)
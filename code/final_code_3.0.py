# Paul Schakel
# Final code for drone 3.0 using N-Channel MOSFETs

import board
import pwmio
import adafruit_mpu6050
import busio
import time 

MOTOR_1 = board.GP11
MOTOR_2 = board.GP21
MOTOR_3 = board.GP20
MOTOR_4 = board.GP10
motor1_pwm = pwmio.PWMOut(MOTOR_1, frequency=1000)
motor2_pwm = pwmio.PWMOut(MOTOR_2, frequency=1000)
motor3_pwm = pwmio.PWMOut(MOTOR_3, frequency=1000)
motor4_pwm = pwmio.PWMOut(MOTOR_4, frequency=1000)

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

while True:
    motor1_pwm.duty_cycle = 65535 // 2  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    motor2_pwm.duty_cycle = 65535 // 2  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    motor3_pwm.duty_cycle = 65535 // 2  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    motor4_pwm.duty_cycle = 65535 // 2  # Cycles the pin with 50% duty cycle (half of 2 ** 16)

    time.sleep(0.2)
    print(f"x: {round(mpu.acceleration[0], 3)} y: {round(mpu.acceleration[1], 3)} z: {round(mpu.acceleration[2], 3)}")

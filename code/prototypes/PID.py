# Paul Schakel
# Prototype for PID control

import board
import pwmio
import adafruit_mpu6050
import busio
import time
import math

MOTOR_1 = board.GP20
MOTOR_2 = board.GP21
MOTOR_3 = board.GP10
MOTOR_4 = board.GP11
motor1_pwm = pwmio.PWMOut(MOTOR_1, frequency=1000)
motor2_pwm = pwmio.PWMOut(MOTOR_2, frequency=1000)
motor3_pwm = pwmio.PWMOut(MOTOR_3, frequency=1000)
motor4_pwm = pwmio.PWMOut(MOTOR_4, frequency=1000)

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

last_update = time.monotonic()
integral_pitch = 0
integral_roll = 0
integral_yaw = 0

throttle = 0

Kp = 1
Ki = 1
Kd = 1

pitch_force = 0

setpoint = 0

pitch_PID = 0
roll_PID = 0
yaw_PID = 0

while True:
    x = mpu.acceleration[0]
    y = mpu.acceleration[1]
    if x == 0:
        x = 0.000001
    initial_angle = math.degrees(math.atan(y/x))
    initial_intensity = math.sqrt((x**2) + (y**2))

    # need to account for angles beyond 90

    now = time.monotonic()
    dt = now - last_update
    

    error_y = setpoint - mpu.acceleration[1]

    #motor1_pwm.duty_cycle = 65535  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    #motor2_pwm.duty_cycle = 65535  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    #motor3_pwm.duty_cycle = 65535  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    #motor4_pwm.duty_cycle = 65535  # Cycles the pin with 50% duty cycle (half of 2 ** 16)

    time.sleep(0.07)
    print("angle: " + str(initial_angle))
    print("initial_intensity: " + str(initial_intensity))
    #print(f"x: {round(mpu.acceleration[0], 3)} y: {round(mpu.acceleration[1], 3)} z: {round(mpu.acceleration[2], 3)}")

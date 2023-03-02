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

Kp = 0.5
Ki = 0.01
Kd = 0.01

error_pitch = 0
error_roll = 0
error_yaw = 0

last_error_pitch = 0
last_error_roll = 0
last_error_yaw = 0

integral_pitch = 0
integral_roll = 0
integral_yaw = 0

derivative_pitch = 0
derivative_roll = 0
derivative_yaw = 0

throttle = 0

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
    angle = math.degrees(math.atan(y/x))
    intensity = math.sqrt((x**2) + (y**2))

    # Find quadrant and make angle between 0 and 360
    if x < 0 and y > 0: # Q2
        angle += 180
    elif x < 0 and y < 0: # Q3
        angle += 180
    elif x > 0 and y < 0: #Q4
        angle += 360

    now = time.monotonic()
    dt = now - last_update
    
    ## Find errors for pitch
    #if angle > 0 and angle < 180:
    #    error_pitch = -1 * (setpoint - intensity)
    #elif angle > 180 and angle < 360:
    #    error_pitch = setpoint - intensity
    #else:
    #    error_pitch = 0

    ## Find errors for roll
    #if angle > 105 and angle < 165:
    #    error_roll = -1 * (setpoint - intensity)
    #elif angle > 285 and angle < 345:
    #    error_roll = setpoint - intensity
    #else:
    #    error_roll = 0

    ## Find errors for pitch and roll at the same time for specific angles
    #if angle >= 345 or angle <= 15:
    #    error_pitch = -1 * (setpoint - intensity)
    #    error_roll = setpoint - intensity
    #if angle >= 75 and angle <= 105:
    #    error_pitch = -1 * (setpoint - intensity)
    #    error_roll = error_pitch
    #if angle >= 165 and angle <= 195:
    #    error_pitch = setpoint - intensity
    #    error_roll = -1 * (setpoint - intensity)
    #if angle >= 255 and angle <= 285:
    #    error_pitch = setpoint - intensity
    #    error_roll = setpoint - intensity

    error_pitch = setpoint - (intensity * math.cos(angle))
    error_roll = setpoint - (intensity * math.sin(angle))

    integral_pitch = integral_pitch + dt * error_pitch
    integral_roll = integral_roll + dt * error_roll

    derivative_pitch = (error_pitch - last_error_pitch)/dt
    derivative_roll = (error_roll - last_error_roll)/dt

    pitch_PID =  Kp * error_pitch + Ki * integral_pitch + Kd * derivative_pitch
    roll_PID = Kp * error_roll + Ki * integral_roll + Kd * derivative_roll

    

    motor1_pwm.duty_cycle = 65535 // 4  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    motor2_pwm.duty_cycle = 65535 // 4  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    motor3_pwm.duty_cycle = 65535 // 4  # Cycles the pin with 50% duty cycle (half of 2 ** 16)
    motor4_pwm.duty_cycle = 65535 // 4  # Cycles the pin with 50% duty cycle (half of 2 ** 16)

    last_error_pitch = error_pitch
    last_error_roll = error_roll
    last_update = now

    time.sleep(0.07)
    print("angle: " + str(angle))
    print("initial_intensity: " + str(intensity))
    print("error_pitch: " + str(error_pitch))
    print("error_roll: " + str(error_roll))
    #print(f"x: {round(mpu.acceleration[0], 3)} y: {round(mpu.acceleration[1], 3)} z: {round(mpu.acceleration[2], 3)}")

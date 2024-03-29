# Paul Schakel
# Prototype for PID control

import board
import pwmio
from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32
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

sda_pin = board.GP16
scl_pin = board.GP17
i2c = busio.I2C(scl_pin, sda_pin)

sensor = LSM6DSO32(i2c)

last_update = time.monotonic()

Kp = 0.3
Ki = 0.05
Kd = 0.3

motor1_baseline = .7
motor2_baseline = .7
motor3_baseline = .7
motor4_baseline = .7

PID_multiplier = 800

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
    x = sensor.acceleration[0]
    y = sensor.acceleration[1]
    if x == 0:
        x = 0.000001
    angle = math.degrees(math.atan(y/x))
    intensity = math.sqrt((x**2) + (y**2))

    if intensity > 9.8:
        intensity = 9.8

    # Find quadrant and make angle between 0 and 360
    if x < 0 and y > 0: # Q2
        angle += 360
    elif x > 0 and y > 0: # Q3
        angle += 180
    elif x > 0 and y < 0: #Q4
        angle += 180

    now = time.monotonic()
    dt = now - last_update

    angle += 45

    if angle > 360:
        angle -= 360

    error_pitch = setpoint - (intensity * math.cos(math.radians(angle)))
    error_roll = setpoint - (intensity * math.sin(math.radians(angle)))

    integral_pitch = integral_pitch + dt * error_pitch
    integral_roll = integral_roll + dt * error_roll

    derivative_pitch = (error_pitch - last_error_pitch)/dt
    derivative_roll = (error_roll - last_error_roll)/dt

    pitch_PID =  Kp * error_pitch + Ki * integral_pitch + Kd * derivative_pitch
    roll_PID = Kp * error_roll + Ki * integral_roll + Kd * derivative_roll

    PID_scaler = PID_multiplier * intensity

    motor1_duty_cycle = int(65535 * motor1_baseline - pitch_PID * PID_scaler)
    motor2_duty_cycle = int(65535 * motor2_baseline - roll_PID * PID_scaler)
    motor3_duty_cycle = int(65535 * motor3_baseline + pitch_PID * PID_scaler)
    motor4_duty_cycle = int(65535 * motor4_baseline + roll_PID * PID_scaler)

    if motor1_duty_cycle > 65535:
        motor1_duty_cycle = 65535
    if motor2_duty_cycle > 65535:
        motor2_duty_cycle = 65535
    if motor3_duty_cycle > 65535:
        motor3_duty_cycle = 65535
    if motor4_duty_cycle > 65535:
        motor4_duty_cycle = 65535
    if motor1_duty_cycle < 2000:
        motor1_duty_cycle = 2000
    if motor2_duty_cycle < 2000:
        motor2_duty_cycle = 2000
    if motor3_duty_cycle < 2000:
        motor3_duty_cycle = 2000
    if motor4_duty_cycle < 2000:
        motor4_duty_cycle = 2000


    print("\nmotor1_pwm.duty_cycle: " + str(motor1_duty_cycle))
    print("motor3_pwm.duty_cycle: " + str(motor3_duty_cycle))

    motor1_pwm.duty_cycle = motor1_duty_cycle
    motor2_pwm.duty_cycle = motor2_duty_cycle
    motor3_pwm.duty_cycle = motor3_duty_cycle
    motor4_pwm.duty_cycle = motor4_duty_cycle
    last_error_pitch = error_pitch
    last_error_roll = error_roll
    last_update = now

    time.sleep(.07)

    #print("\nangle: " + str(angle))
    #print("pitch_PID: " + str(pitch_PID))
    #print("integral_pitch: " + str(integral_pitch))
    #print("derivative_pitch: " + str(derivative_pitch))
    #print("error_pitch: " + str(error_pitch))

    #temp_baseline = float(input("Enter baseline: "))
    #motor1_baseline = temp_baseline
    #motor2_baseline = temp_baseline
    #motor3_baseline = temp_baseline
    #motor4_baseline = temp_baseline

    #print(f"x: {round(sensor.acceleration[0], 3)} y: {round(sensor.acceleration[1], 3)} z: {round(sensor.acceleration[2], 3)}")

#type: ignore
# Paul Schakel
# Prototype for PID control

import board
import pwmio
from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32
import busio
import time
import math

MOTOR_1 = board.GP11
MOTOR_2 = board.GP21
MOTOR_3 = board.GP10
MOTOR_4 = board.GP20
motor1_pwm = pwmio.PWMOut(MOTOR_1, frequency=1000)
motor2_pwm = pwmio.PWMOut(MOTOR_2, frequency=1000)
motor3_pwm = pwmio.PWMOut(MOTOR_3, frequency=1000)
motor4_pwm = pwmio.PWMOut(MOTOR_4, frequency=1000)

sda_pin = board.GP16
scl_pin = board.GP17
i2c = busio.I2C(scl_pin, sda_pin)

sensor = LSM6DSO32(i2c)

last_update = time.monotonic()
start_time = time.monotonic()

Kp = 0.23
Ki = 0.1 #decrease Ki
Kd = 0.0

motor_baseline = 0

PID_multiplier = 1000

error_pitch = 0
error_roll = 0
error_yaw = 0

last_errors_pitch = []
last_errors_roll = []
last_errors_yaw = []

avg_error_pitch = 0
avg_error_roll = 0
avg_error_yaw = 0

last_avg_error_pitch = 0
last_avg_error_roll = 0
last_avg_error_yaw = 0

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

pitch_data = []
roll_data = []

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

    angle -= 45

    if angle > 360:
        angle -= 360

    run_time = now - start_time

    if run_time < 2:
        if motor_baseline < 0.7:
            motor_baseline += 0.005
    if run_time > 2 and run_time < 4:
        if motor_baseline > 0.1:
            motor_baseline -= 0.005
    if run_time > 4:
        break
        

    error_pitch = setpoint - (intensity * math.cos(math.radians(angle)))
    last_errors_pitch.append(error_pitch)
    avg_error_pitch = sum(last_errors_pitch) / len(last_errors_pitch)
    error_roll = setpoint - (intensity * math.sin(math.radians(angle)))
    last_errors_roll.append(error_roll)
    avg_error_roll = sum(last_errors_roll) / len(last_errors_roll)

    integral_pitch = integral_pitch + dt * avg_error_pitch
    integral_roll = integral_roll + dt * avg_error_roll

    derivative_pitch = (avg_error_pitch - last_avg_error_pitch)/dt
    derivative_roll = (avg_error_roll - last_avg_error_roll)/dt

    pitch_PID =  Kp * avg_error_pitch + Ki * integral_pitch + Kd * derivative_pitch
    roll_PID = Kp * avg_error_roll + Ki * integral_roll + Kd * derivative_roll

    PID_scaler = PID_multiplier * intensity

    motor1_duty_cycle = int(65535 * motor_baseline - pitch_PID * PID_scaler)
    motor2_duty_cycle = int(65535 * motor_baseline - roll_PID * PID_scaler)
    motor3_duty_cycle = int(65535 * motor_baseline + pitch_PID * PID_scaler)
    motor4_duty_cycle = int(65535 * motor_baseline + roll_PID * PID_scaler)

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
    print("motor2_pwm.duty_cycle: " + str(motor2_duty_cycle))
    print("motor4_pwm.duty_cycle: " + str(motor4_duty_cycle))
    print("motor_baseline: " + str(motor_baseline))
    #print("roll_PID: " + str(roll_PID))
    print("pitch_PID: " + str(pitch_PID))

    motor1_pwm.duty_cycle = motor1_duty_cycle   #setting motor speeds
    motor2_pwm.duty_cycle = motor2_duty_cycle
    motor3_pwm.duty_cycle = motor3_duty_cycle
    motor4_pwm.duty_cycle = motor4_duty_cycle
    last_update = now
    last_avg_error_pitch = avg_error_pitch
    last_avg_error_roll = avg_error_roll

    if len(last_errors_pitch) > 5:
        last_errors_pitch.pop(0)
    if len(last_errors_roll) > 5:
        last_errors_roll.pop(0)

    pitch_data.append(error_pitch)
    roll_data.append(error_roll)

        


with open("/error.txt", "a") as datalog:
    motor1_pwm.duty_cycle = 0   #setting motor speeds
    motor2_pwm.duty_cycle = 0
    motor3_pwm.duty_cycle = 0
    motor4_pwm.duty_cycle = 0
    datalog.write('Pitch_Error,Roll_Error\n')  #title for the log file
    datalog.flush()
    for i in range(len(pitch_data)):
        datalog.write('{},{}\n'.format(pitch_data[i], roll_data[i]))  #storing error data on the log file
        datalog.flush()

        #time.sleep(.08)
        #print("\nangle: " + str(angle))
        #print("pitch_PID: " + str(pitch_PID))
        #print("integral_pitch: " + str(integral_pitch))
        #print("derivative_pitch: " + str(derivative_pitch))
        #print("avg_error_pitch: " + str(avg_error_pitch))

        #temp_baseline = float(input("Enter baseline: "))
        #motor1_baseline = temp_baseline
        #motor2_baseline = temp_baseline
        #motor3_baseline = temp_baseline
        #motor4_baseline = temp_baseline

        #print(f"x: {round(sensor.acceleration[0], 3)} y: {round(sensor.acceleration[1], 3)} z: {round(sensor.acceleration[2], 3)}")

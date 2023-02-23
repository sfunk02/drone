# Paul Schakel
# Final code for the drone 2.0 using the TB6612FNG

from adafruit_motor import motor
import board
import busio
import adafruit_mpu6050
import pwmio
import digitalio
import time 

PWM_FREQ = 1000

A1 = board.GP10
A2 = board.GP11
B1 = board.GP12
B2 = board.GP13
C1 = board.GP18
C2 = board.GP19
D1 = board.GP20
D2 = board.GP21
PWMA = board.GP27
PWMB = board.GP26
PWMC = board.GP16
PWMD = board.GP17

motorA_pin1 = digitalio.DigitalInOut(A1)
motorA_pin1.direction = digitalio.Direction.OUTPUT
motorA_pin2 = digitalio.DigitalInOut(A2)
motorA_pin2.direction = digitalio.Direction.OUTPUT
motorA_pin1.pull = digitalio.Pull.UP
motorA_pin2.pull = digitalio.Pull.DOWN
motorA_pwm = pwmio.PWMOut(PWMA, frequency=PWM_FREQ)

motorB_pin1 = digitalio.DigitalInOut(B1)
motorB_pin1.direction = digitalio.Direction.OUTPUT
motorB_pin2 = digitalio.DigitalInOut(B2)
motorB_pin2.direction = digitalio.Direction.OUTPUT
motorB_pin1.pull = digitalio.Pull.DOWN
motorB_pin2.pull = digitalio.Pull.UP
motorB_pwm = pwmio.PWMOut(PWMB, frequency=PWM_FREQ)

motorC_pin1 = digitalio.DigitalInOut(C1)
motorC_pin1.direction = digitalio.Direction.OUTPUT
motorC_pin2 = digitalio.DigitalInOut(C2)
motorC_pin2.direction = digitalio.Direction.OUTPUT
motorC_pin1.pull = digitalio.Pull.UP
motorC_pin2.pull = digitalio.Pull.DOWN
motorC_pwm = pwmio.PWMOut(PWMC, frequency=PWM_FREQ)

motorD_pin1 = digitalio.DigitalInOut(D1)
motorD_pin1.direction = digitalio.Direction.OUTPUT
motorD_pin2 = digitalio.DigitalInOut(D2)
motorD_pin2.direction = digitalio.Direction.OUTPUT
motorD_pin1.pull = digitalio.Pull.DOWN
motorD_pin2.pull = digitalio.Pull.UP
motorD_pwm = pwmio.PWMOut(PWMD, frequency=PWM_FREQ)

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

throttle_speed = 0

while True:
    motorA_pwm.duty_cycle = 65535 // 2
    motorB_pwm.duty_cycle = 65535 // 2
    motorC_pwm.duty_cycle = 65535 // 2
    motorD_pwm.duty_cycle = 65535 // 2

    #time.sleep(0.2)
    #print(f"x: {round(mpu.acceleration[0], 3)} y: {round(mpu.acceleration[1], 3)} z: {round(mpu.acceleration[2], 3)}")
    #motor1.throttle = mpu.acceleration[1] / 10.0

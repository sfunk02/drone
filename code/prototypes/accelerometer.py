# Paul Schakel
# Prototype code for the MPU6050 accelerometer -- just prints out acceleration values ad infinitum

import adafruit_mpu6050
import board
import busio
import time

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

while True:
    print(f"x: {round(mpu.acceleration[0], 3)} y: {round(mpu.acceleration[1], 3)} z: {round(mpu.acceleration[2], 3)}")
    time.sleep(0.2)
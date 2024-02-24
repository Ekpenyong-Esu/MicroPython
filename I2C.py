"""P9-1 Attempt a write to a non-existing device"""
from machine import Pin, I2C

i2c = I2C(1, scl = Pin(27), sda = Pin(26), freq = 400_000)
DEV_ADDR = 0x55

# Write to a non-existing device to cause an OSError
i2c.writeto(DEV_ADDR, b'0')

# This line will not be executed because of the previous error
print('Write to device', hex(DEV_ADDR), 'successfully')

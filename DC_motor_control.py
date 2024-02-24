"""Program 10-1 DC Motor Direction Control"""

import time
from machine import Pin

m1 = Pin(18, Pin.OUT)
m2 = Pin(19, Pin.OUT)
pwm12 = Pin(16, Pin.OUT)  # PWM power control for M1 and M2
pwm12.on()                # keep PWM signal high

while True:
    # Current flows from M1 to M2
    m1.on()
    m2.off()
    time.sleep(1)
    # Current flow stops
    m1.on()
    m2.on()
    time.sleep(0.5)
    # Current flows from M2 to M1
    m1.off()
    m2.on()
    time.sleep(1)
    # Current flow stops
    m1.on()
    m2.on()
    time.sleep(0.5)

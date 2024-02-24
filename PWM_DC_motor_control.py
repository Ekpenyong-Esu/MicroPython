"""Program 11-2 DC Motor Speed Control"""

import time
from machine import Pin, PWM

m1 = Pin(18, Pin.OUT)
m2 = Pin(19, Pin.OUT)

pwmA = PWM(Pin(3))   # PWM power control for H bridge A
pwmA.freq(500)

while True:
    # Current flows from AO1 to AO2
    m1.on()
    m2.off()

    # Stepping up the dutycycle; ramp up the speed
    for i in range(0, 65535, 500):
        pwmA.duty_u16(i)
        time.sleep(0.02)

    # Stepping down the dutycycle; ramp down the speed
    for i in range(65535, 0, -500):
        pwmA.duty_u16(i)
        time.sleep(0.02)

    # Current flows from AO2 to AO1
    m2.on()
    m1.off()

    # Stepping up the dutycycle; ramp up the speed
    for i in range(0, 65535, 500):
        pwmA.duty_u16(i)
        time.sleep(0.02)

    # Stepping down the dutycycle; ramp down the speed
    for i in range(65535, 0, -500):
        pwmA.duty_u16(i)
        time.sleep(0.02)

"""Program 11-1: Using PWM to modulate the brightness of the LED"""

import time
from machine import Pin, PWM

pwm = PWM(Pin(3))   # Define the GPIO pin connected to the LED

# Set the frequency of the PWM signal
# Adjust the frequency as needed
pwm.freq(500)

while True:
    # Stepping up the duty cycle
    for i in range(0, 65535, 500):   # Range from 0 to 65535 (16-bit)
        pwm.duty_u16(i)
        time.sleep(0.02)

    # Stepping down the duty cycle
    for i in range(65535, 0, -500):
        pwm.duty_u16(i)
        time.sleep(0.02)

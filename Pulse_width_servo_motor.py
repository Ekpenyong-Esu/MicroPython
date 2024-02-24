"""Program 11-3: Using PWM to Control a Servomotor"""

import time
from machine import Pin, PWM

pwm = PWM(Pin(3))   # control pin
pwm.freq(50)         # 20ms period

while True:
    # Stepping up the positive pulse width from 1ms to 2ms
    for pw in range(1_000_000, 2_000_000, 10_000):
        pwm.duty_ns(pw)
        time.sleep(0.02)

    # Stepping down the positive pulse width from 2ms to 1ms
    for pw in range(2_000_000, 1_000_000, -10_000):
        pwm.duty_ns(pw)
        time.sleep(0.02)

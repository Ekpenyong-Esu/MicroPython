"""Program 10-3 Stepper motor control reverse direction"""

import time
from machine import Pin

# Initialize motor control pins in a list
MOTOR_PINS = (18, 19, 20, 21)
motor_pin_list = []
for pin in MOTOR_PINS:
    motor_pin_list.append(Pin(pin, Pin.OUT))

# Initinalize PWM power control pins
pwmA = Pin(16, Pin.OUT)  # PWM power control for A
pwmB = Pin(17, Pin.OUT)  # PWM power control for B
# Keep PWM pins high all the time
pwmA.on()
pwmB.on()

steps = (0x9, 0x5, 0x6, 0xa)

def stepping(step):
    """Making one step of the motor"""
    for index, pin in enumerate(motor_pin_list):
        on_off = step & (1 << index)
        pin.value(on_off)
    time.sleep_ms(200)

while True:
    # Turning one direction for 32 steps
    for i in range(32 // 4):
        for step in steps:    # make four steps
            stepping(step)
    time.sleep_ms(500)

    # Reverse the direction for 32 steps
    for i in range(32 // 4):
        for step in reversed(steps): # make four steps
            stepping(step)
    time.sleep_ms(500)

"""Program 10-2 Stepper motor control"""

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

# Select one of the stepping sequences below
#halfsteps = (0x9, 0x1, 0x5, 0x4, 0x6, 0x2, 0xa, 0x8)
steps = (0x9, 0x5, 0x6, 0xa)

while True:
    for step in steps:
        for index, pin in enumerate(motor_pin_list):
            on_off = step & (1 << index)
            #print(index, pin, step, 1 << index, on_off)
            pin.value(on_off)
        time.sleep_ms(200)

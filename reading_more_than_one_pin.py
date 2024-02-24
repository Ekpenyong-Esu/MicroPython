"""Program 2-10 Reading two switches and blinking corresponding LEDs"""

import time
from machine import Pin

def blink(led):
    """Blink an LED"""
    for i in range(0, 3):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

led1 = Pin(22, Pin.OUT)
led2 = Pin(26, Pin.OUT)

switch1 = Pin(14, Pin.IN, Pin.PULL_DOWN)
switch2 = Pin(15, Pin.IN, Pin.PULL_DOWN)

while True:
    if switch1.value():
        blink(led1)
    if switch2.value():
        blink(led2)

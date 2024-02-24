"""Program 5-1: Blink the green LED on a Pico board"""

import time
from machine import Pin

LED = Pin("LED", Pin.OUT)

while True:
    LED.on()
    time.sleep(0.5)
    LED.off()
    time.sleep(0.5)

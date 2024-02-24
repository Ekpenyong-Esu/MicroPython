"""Program 5-2: Toggle a GPIO pin of a Pico board"""

import time
from machine import Pin

LED = Pin("LED", Pin.OUT)

while True:
    LED.toggle()
    time.sleep_ms(50)

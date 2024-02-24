"""Program 2-7: Toggling multiple LED_list sequentially"""

import time
from machine import Pin

# make a tuple of pins used
LED_pins = (22,  "LED", 26, 27, 28)

# start with an empty list
LED_list = []

# add objects of pins used to the list
for p in LED_pins:
    LED_list.append(Pin(p, Pin.OUT))

# turn one LED on at a time
while True:
    for LED in LED_list:
        LED.on()
        time.sleep(0.5)
        LED.off()

# turn all LEDs on at the same time
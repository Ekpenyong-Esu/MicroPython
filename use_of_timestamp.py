"""Program 5-7: Use of timestamps to Measure Elapsed Time
   Measure time a switch is depressed.
"""

import time
from machine import Pin

sw = Pin(15, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

depressed = False

while True:
    led.value(sw.value())                    # LED reflect the state of the switch

    if not depressed and sw.value() == 0:    # switch depressed
        before = time.ticks_ms()
        time.sleep_ms(10)                    # debounce
        depressed = True

    if depressed and sw.value() == 1:        # switch released
        after = time.ticks_ms()
        timelapsed = time.ticks_diff(after, before)
        print('switch was depressed for', timelapsed, 'ms')
        time.sleep_ms(10)                    # debounce
        depressed = False

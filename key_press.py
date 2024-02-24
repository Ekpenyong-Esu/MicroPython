"""Program 3-6 Function keypressed returns true when one of the
           keys is pressed, false when no key is pressed.

    Wiring of the keypad to Pico board GPIO pins
    col 1 - GP6
    col 2 - GP7
    col 3 - GP8
    col 4 - GP9
    row 1 - GP10
    row 2 - GP11
    row 3 - GP12
    row 4 - GP13
"""

import time
from machine import Pin

# four GPIO pins connected to four column
colGpPins = (6, 7, 8, 9)
# four GPIO pins connected to four rows
rowGpPins = (10, 11, 12, 13)

# Empty list for column pin objects
colPins = []
# Construct the list of column pin objects
for p in colGpPins:
    colPins.append(Pin(p, Pin.IN, Pin.PULL_UP))

# Empty list for row pin objects
rowPins = []
# Construct the list of row pin objects
for p in rowGpPins:
    rowPins.append(Pin(p, Pin.IN))

def keypressed():
    """Function to scan the keypad to see whether a key is pressed"""
    # Make all row pins output and set them low
    for row in rowPins:
        row.init(Pin.OUT)
        row.off()

    # wait for signals to settle
    time.sleep_us(10)

    # scan one column at a time
    for col in colPins:
        if col.value() == 0:
            return True   # if a column is low

    return False          # no column was low

# code to test function keypressed
while True:
    if keypressed():
        print('X')        # if a key is pressed
    else:
        print('O')        # no key is pressed

    time.sleep_ms(100)

""" Program 3-7 Non-blocking function getkey detects key press,
          when a key is pressed, return the key label.
          If no key is pressed, return 0.

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

# make a tuple of key labels by row
keyLabel = '123A', '456B', '789C', '0FED'

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

def get_key():
    """Scan keypad to find the key that is pressed"""
    # Make row pins output and set them low
    for row in rowPins:
        row.init(Pin.OUT)
        row.off()
        time.sleep_us(10)   # wait for signal to settle

        # scan columns to see whether a key is pressed
        for col in colPins:
            if col.value() == 0:
                # if a column is low, a key is pressed
                row.init(Pin.IN)   # restore the row pin to input
                # use row and column number as index to find the key label
                return keyLabel[rowPins.index(row)][colPins.index(col)]
        # restore the row pin to input
        row.init(Pin.IN)

    return 0    # if no key was found pressed


while True:
    key = get_key()    # read the keypad

    if key != 0:                # if a key is pressed
        print(key, end = '')    # print the key label without newline
        time.sleep_ms(10)       # wait for key contact bounce
        while get_key() != 0:   # wait until the key is released
            pass
        time.sleep_ms(10)       # wait for key contact bounce

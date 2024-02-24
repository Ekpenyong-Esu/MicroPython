"""Program 7-2: Perform A-to-D conversion on GP26 pin.
   GP26 pin is connected to a potentiometer.
"""

import time
from machine import ADC, Pin

pot = ADC(Pin(26))   # instantiate an ADC object using GP26 pin.

while True:
    value = pot.read_u16()       # read a conversion result
    #value &= 0xFFF0              # mask out the lower bits
    volts = value * 3.3 / 65520  # convert to volts
#    print('{:2.2f} V'.format(volts)) # MicroPython v1.16 or earlier
    print(f'{volts:2.2f} V')     # MicroPython v1.17 or later
    time.sleep(1)

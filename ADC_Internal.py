"""Program 7-1: Perform A-to-D conversion on GP29 pin.
   GP29 pin is connected to VSYS/3 on the Pico board.
"""

import time
from machine import ADC, Pin

vsys = ADC(Pin(29))   # instantiate an ADC object using GP29 pin.

while True:
    value = vsys.read_u16()          # read a conversion result
    #value &= 0xFFF0                  # mask out the lower bits
    volts = (value / 65520) * 3.3      # convert to volts
    volts *= 3                       # multiply by 3 to get VSYS
#    print("%4.2f V" % volts)         # lagacy format
#    print('{:2.2f} V'.format(volts)) # MicroPython v1.16 or earlier
    print(f'{volts:2.2f} V')         # MicroPython v1.17 or later
    time.sleep(1)

"""Program 7-3: Perform A-to-D conversion on GP27 pin.
   GP27 pin is connected to an LM34 temperature sensor.
"""

import time
from machine import ADC, Pin

LM34 = ADC(Pin(27))   # instantiate an ADC object using GP27 pin.

while True:
    value = LM34.read_u16()    # read a conversion result
    #value &= 0xFFF0            # mask out the lower bits
    mV = (value / 65520) * 3.3  # convert to millivolts
    temp = mV * 100             # Convert voltage to temperature in Fahrenheit
#    print('{:3.1f} F'.format(temp)) # MicroPython v1.16 or earlier
    print(f'{temp:3.1f} F')    # MicroPython v1.17 or later
    time.sleep(1)

""" Program 7-4: Perform A-to-D conversion on the internal temperature sensor.
"""

import time
from machine import ADC

sensor = ADC(ADC.CORE_TEMP)      # instantiate an ADC object using GP27 pin.

while True:
    value = sensor.read_u16()    # read a conversion result
   
    volts = (value  / 65535) * 3.3  # convert to volts
    temp = 27 - (volts - 0.706) / 0.001721 # from RP2040 datasheet
#    print('{:3.1f} C'.format(temp))        # MicroPython v1.16 or earlier
    print(f'{temp:3.1f} C')                # MicroPython v1.17 or later
    time.sleep(1)

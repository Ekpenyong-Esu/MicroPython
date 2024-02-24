"""Program 5-8: Reading Real-time clock."""

import time
from machine import RTC

rtc = RTC()   # instantiate a real-time clock

while True:
    tt = rtc.datetime()  # read time tuple
    print(tt)            # print time tuple
    time.sleep(1)

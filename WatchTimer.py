"""Program 5-9: Demonstrate the use of Watchdog Timer"""

import time
from machine import WDT

# enable the WDT and set the timeout to 5s
wdt = WDT(timeout = 5000)

for i in range(0, 10):
    wdt.feed()
    print(i)
    time.sleep_ms(i * 1000)

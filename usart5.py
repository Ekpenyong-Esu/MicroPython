"""Program 4-5: Loopback test. Explore the readline() function.
           Put a jumper between the GP5 pin and the GP4 pin.
"""

import time
from machine import UART, Pin
from utime import sleep_ms

uart1 = UART(1, baudrate = 9600, rx = Pin(5), tx = Pin(4))
m = uart1.write("ABCDEFGHIJKLMNO\nPQRSTUVWXYZ")
sleep_ms(30)
n = uart1.readline()
print (m, n)
p = uart1.readline()
print (p)

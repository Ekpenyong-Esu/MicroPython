"""Program 4-4: Loopback test. Explore the readinto() function.
           Put a jumper between the GP5 pin and the GP4 pin.
"""

import time
from machine import UART, Pin
from utime import sleep_ms

alphabets = bytearray(12)

uart1 = UART(1, baudrate = 9600, rx = Pin(5), tx = Pin(4))
m = uart1.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
sleep_ms(30)
n = uart1.readinto(alphabets, 10)
print (m, n, alphabets)
p = uart1.readinto(alphabets)
print (p, alphabets)
q = uart1.readinto(alphabets)
print (q, alphabets)

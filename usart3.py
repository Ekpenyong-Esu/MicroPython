"""Program 4-3: Loopback test. Read from the receive buffer.
           Put a jumper between the GP5 pin and the GP4 pin.
"""

import time
from machine import UART, Pin
from utime import sleep_ms

uart1 = UART(1, baudrate = 9600, rx = Pin(5), tx = Pin(4))
m = uart1.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
n = uart1.read()
sleep_ms(10)
p = uart1.read()
sleep_ms(20)
q = uart1.read()

print (m, n, p, q)

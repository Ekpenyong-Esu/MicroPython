"""
Program 4-2: Loopback test. Observe whether the receive buffer is empty.
           Put a jumper between the GP5 pin and the GP4 pin.
"""

import time
from machine import UART, Pin
from utime import sleep_ms

uart1 = UART(1, baudrate = 9600, rx = Pin(5), tx = Pin(4))

send_data = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
uart1.write(send_data)
sleep_ms(50)
rec_data = uart1.read()
print(rec_data.decode('utf-8'))

# m = uart1.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# n = uart1.any()
# time.sleep_ms(10)
# p = uart1.any()
# time.sleep_ms(20)
# q = uart1.any()

# print (m, n, p, q)

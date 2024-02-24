"""Program 4-1: Write 'hello world' to UART1 once every second
            UART1 Tx is assigned to the GP20 pin.
"""

import time
from machine import UART, Pin
from utime import sleep_ms

uart1 = UART(1, baudrate = 9600, tx = Pin(4))

while True:
    uart1.write('hello world\r\n')
    sleep_ms(10)
    n = uart1.read()
    print(n.decode('utf-8'), 'bytes sent')
    time.sleep(1)

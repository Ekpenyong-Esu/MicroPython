"""Program 2-9 Reading the status of a switch"""

from machine import Pin

led = Pin(25, Pin.OUT)
switch = Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    val = switch.value()
    led.value(val)

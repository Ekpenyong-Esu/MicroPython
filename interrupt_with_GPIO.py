"""Program 6-1: Use GPIO pin to generate interrupts"""

import time
from machine import Pin

led = Pin("LED", Pin.OUT)

def pin_handler(pin):
    """Interrupt handler toggles the onboard LED"""
    print(pin)
    led.toggle()

# Setup GP15 pin to generate interrupt at the falling edge of input signal
pin = Pin(15, Pin.IN, Pin.PULL_UP)
pin.irq(handler = pin_handler, trigger = Pin.IRQ_FALLING)

# Foreground task, count down to zero then turn off the interrupt
n = 20
while True:
    time.sleep(1)
    print(n)
    n = n - 1
    if n < 0:
        pin.irq(trigger = 0)  # turn off GPIO pin interrupt
        print('GPIO interrupt disabled.')
        break

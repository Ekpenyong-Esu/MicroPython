"""Program 6-6: Use GPIO pin interrupts to measure input signal frequency.
"""

import time
from machine import Pin, Timer

# Interrupt handler counts the number of pulses
last_timestamp = 0

def pin_handler(_):
    """Pin interrupt handler"""
    global last_timestamp
    current_timestamp = time.ticks_us()
    timelapsed = time.ticks_diff(current_timestamp, last_timestamp)
    last_timestamp = current_timestamp
    frequency = 1000000 / timelapsed
    print('freq =', frequency, 'Hz')

# Setup GP15 pin to trigger interrupt at falling edges
pin = Pin(15, Pin.IN, Pin.PULL_UP)
pin.irq(handler = pin_handler, trigger = Pin.IRQ_FALLING)

# Use Timer to generate a 10 Hz pulse at GP16.
# Install a jumper between GP3 and GP15 to trigger interrupts.
pulse = Pin(3, Pin.OUT)
Timer(period = 50, mode = Timer.PERIODIC,
          callback = lambda t:pulse.toggle())

while True:
    pass

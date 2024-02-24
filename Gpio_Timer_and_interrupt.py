"""Program 6-4: Use Timer to generate a periodic pulse output on a
   GPIO pin, which is used to trigger GPIO pin interrupt on
   the other pin. The interrupt handler counts the number of
   pulses.
"""

from machine import Timer, Pin

# Interrupt handler counts the number of pulses
pinHandler_counter = 0

def pin_handler(_):
    """Pin interrupt handler"""
    global pinHandler_counter
    pinHandler_counter += 1  # increment the counter
    print(pinHandler_counter)

# Setup GP15 pin to trigger interrupt at falling edges
pin = Pin(15, Pin.IN, Pin.PULL_UP)
pin.irq(pin_handler, Pin.IRQ_FALLING)

# Use Timer to generate a 1 Hz pulse at GP16.
# Install a jumper between GP3 and GP15 to trigger interrupts.
pulse = Pin(3, Pin.OUT)
Timer(period = 500, mode = Timer.PERIODIC,
          callback = lambda t:pulse.toggle())

while True:
    pass   # Do nothing

"""Program 6-5: Use Timer to generate a periodic pulse output on a
   GPIO pin, which is used to trigger GPIO pin interrupt on
   the other pin. The interrupt handler counts the number of
   pulses. For every 12 pulses, it unlocks the flag to let the
   thread packaging run once.
"""
import _thread
from machine import Timer, Pin

# Create a lock
flag = _thread.allocate_lock()
flag.acquire() # so that packaging will not run until it is unlocked

# This function will be run as a thread on the second CPU core.
# It waits in an infinite loop for the signal from the interrupt
# handler that 12 widgets had passed then starts the packaging
# procedure.
def packaging():
    """ A function that is supposed to control the packaging machine"""
    while True:
        flag.acquire()  # waiting for the signal
        print("=== Packing up a bag of 12 widgets ===")

# Start packaging() as a new thread
_thread.start_new_thread(packaging, ())

# Interrupt handler counts the number of pulses.
# After every 12 counts, unlock the lock so that packaging will run.
pinHandler_counter = 0
def pin_handler(_):
    """Pin interrupt handler"""
    global pinHandler_counter
    pinHandler_counter += 1    # increment the counter
    print(pinHandler_counter)
    if pinHandler_counter >= 12:
        flag.release()         # after every 12 counts, unlock
        pinHandler_counter = 0 # reset the counter

# Setup GP15 pin to trigger interrupt at falling edges
pin = Pin(15, Pin.IN, Pin.PULL_UP)
pin.irq(pin_handler, Pin.IRQ_FALLING)

# Use Timer to generate a 2 Hz pulse at GP16.
# Install a jumper between GP3 and GP15 to trigger interrupts.
pulse = Pin(3, Pin.OUT)
Timer(period = 250, mode = Timer.PERIODIC,
          callback = lambda t:pulse.toggle())

# The foreground task may run the user interface.
while True:
    pass   # Do nothing for now

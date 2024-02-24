"""Program 6-2: Use GPIO pin to generate interrupts with
                a foreground task occupying the CPU all the time.
"""

from machine import Pin

led = Pin(3, Pin.OUT)

def pin_handler(_):
    """Interrupt handler toggles the onboard LED"""
    led.toggle()

# Setup GP15 pin to generate interrupt at a falling edge
pin = Pin(15, Pin.IN, Pin.PULL_UP)
pin.irq(pin_handler, Pin.IRQ_FALLING)


def is_prime(num):
    """function to find all prime numbers"""
    # all prime numbers are greater than 1
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
    return True

# Foreground task to find all the prime number by brute force
num = 2
while True:
    if is_prime(num):
        print(num)
    num += 1

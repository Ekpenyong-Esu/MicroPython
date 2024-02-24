"""Program 2-2: Toggling green LED on a Pico board at 1 Hz"""

from machine import Pin

def delay():
    """500 ms delay at 125,000,000 Hz CPU frequency"""
    for i in range(0, 95_785):
        pass

LED = Pin(16)
LED.init(Pin.OUT)

while True:
    LED.on()
    delay()
    LED.off()
    delay()

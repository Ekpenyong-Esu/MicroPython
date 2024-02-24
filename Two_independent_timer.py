"""Program 5-4: Two Independent Timers
  Connect an LED to pin 16 and one to pin 17 of the Pico board
"""

from machine import Timer, Pin

LED0 = Pin("LED", Pin.OUT)
LED1 = Pin(3, Pin.OUT)

def blink0(_):
    """ blink LED0"""
    LED0.toggle()

def blink1(_):
    """ blink LED1"""
    LED1.toggle()

tm1 = Timer(period = 473, mode = Timer.PERIODIC, callback = blink0)
tm2 = Timer(period = 513, mode = Timer.PERIODIC, callback = blink1)

while True:
    name = input('What is your name? ')
    print('Hello', name, '!')
    if name == 'Bob':
        break  # Break out of the loop when 'Bob' is entered

tm1.deinit()    # stop timer 1
tm2.deinit()    # stop timer 2
print('Bye!')

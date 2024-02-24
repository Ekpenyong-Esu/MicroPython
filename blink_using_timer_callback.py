"""Program 5-3: Blink the green LED on a Pico board using Timer callback"""

from machine import Timer, Pin

LED = Pin("LED", Pin.OUT)

def blink(_):
    """ blink the LED"""
    LED.toggle()

tm = Timer(period = 500, mode = Timer.PERIODIC, callback = blink)

while True:
    name = input('What is your name? ')
    print('Hello', name, '!')
    if name == 'Bob':
        break  # Break out of the loop when 'Bob' is entered

tm.deinit()    # stop the timer
print('Bye!')

"""Program 5-6: Blink the green LED on a Pico board for 100 ms every second
   This program demonstrates the use of a lambda function.
"""

from machine import Timer, Pin

LED = Pin("LED", Pin.OUT)
    
def turn_on_LED(_):
    """Turn on LED and set a oneshot timer to turn it off.
       Demonstrate the use of lambda function."""
    LED.on()
    Timer(period = 100, mode = Timer.ONE_SHOT, callback = lambda t : LED.off())

tm = Timer(period = 1000, mode = Timer.PERIODIC, callback = turn_on_LED)

while True:
    name = input('What is your name? ')
    print('Hello', name, '!')
    if name == 'Bob':
        break  # Break out of the loop when 'Bob' is entered

tm.deinit()    # stop the timer
print('Bye!')

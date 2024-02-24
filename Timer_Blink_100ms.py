"""Program 5-5: Blink the green LED on a Pico board for 100 ms every second
"""

from machine import Timer, Pin

LED = Pin("LED", Pin.OUT)

def turn_off_LED(_):
    """Turn off LED"""
    LED.off()
    
def turn_on_LED(_):
    """Turn on LED and set a oneshot timer to turn it off"""
    LED.on()
    Timer(period = 100, mode = Timer.ONE_SHOT, callback = turn_off_LED)

tm = Timer(period = 1000, mode = Timer.PERIODIC, callback = turn_on_LED)

while True:
    name = input('What is your name? ')
    print('Hello', name, '!')
    if name == 'Bob':
        break  # Break out of the loop when 'Bob' is entered

tm.deinit()    # stop the timer
print('Bye!')

"""Program 4-6: Echo - read a character from UART1 and write it back
           Connect the GP4 pin and the GP5 pin to a PC through
           a USB-to-Serial Converter.
"""

from machine import UART, Pin

uart1 = UART(1, baudrate = 9600, rx = Pin(5), tx = Pin(4))

def uart1_get_char():
    """This is a blocking function to get a character from UART1"""
    while True:
        char = uart1.read(1)
        if char is not None:
            print(char.decode('utf-8'))   # for debugging only
            return char

uart1.write('\r\nEnter a string> ')   # display a prompt on the terminal
while True:
    c = uart1_get_char()  # read a character from UART
    uart1.write(c)      # write the character back

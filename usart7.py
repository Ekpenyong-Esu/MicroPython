from machine import UART, Pin

uart1 = UART(0, baudrate=9600, rx=Pin(1), tx=Pin(0))

def uart1_get_char():
    """This is a blocking function to get a character from UART1"""
    while True:
        char = uart1.read(1)
        if char is not None:
            print(char)   # for debugging only
            return char

def uart1_get_line():
    """Read a line ending with a carriage return character ('\r')"""
    s = bytearray()

    while True:
        c = uart1_get_char()

        if c == b'\n':
            #print('eol')  # for debugging only
            return s.decode('utf-8')

        if c == b'\b':
            if len(s) > 0:
                s = s[:-1]
                uart1.write(b'\b \b')
        else:
            uart1.write(c)
            #print(s, c)  # for debugging only
            s = s + c

def uart1_get_number():
    """Read a string from UART1 and convert it to a float number"""
    s = uart1_get_line()
    # print(s, type(s))  # for debugging only
    
    try:
        f = float(s)
        #print(f, type(f))  # for debugging only
        return f
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

uart1.write(b'\r\nPlease enter a number: ')  # prompt in bytes
n = uart1_get_line()

if n is not None:
    #print(n, type(n))  # for debugging only
    uart1.write(n)  # prompt and message in bytes

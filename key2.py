import machine
import utime

# Define the GPIO pins for the keypad rows and columns
ROWS = [0, 1, 2, 3]
COLS = [4, 5, 6, 7]

def setup_keypad():
    # Set up the rows as inputs with pull-up resistors
    for row_pin in ROWS:
        machine.Pin(row_pin, machine.Pin.IN, machine.Pin.PULL_UP)
    
    # Set up the columns as outputs
    for col_pin in COLS:
        machine.Pin(col_pin, machine.Pin.OUT)

def read_keypad():
    for col_pin in COLS:
        machine.Pin(col_pin, machine.Pin.OUT, value=0)
        for row_pin in ROWS:
            if not machine.Pin(row_pin).value():
                return (row_pin, col_pin)
        machine.Pin(col_pin, machine.Pin.OUT, value=1)
    
    return None

# Setup keypad
setup_keypad()

try:
    while True:
        key = read_keypad()
        if key:
            row, col = key
            print(f"Key pressed: Row {row}, Col {col}")
        else:
            print("No key pressed")
        utime.sleep_ms(100)

except KeyboardInterrupt:
    pass
finally:
    # Cleanup if needed
    pass

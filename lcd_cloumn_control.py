"""Program 3-5: Example of Cursor Control"""

import time
from machine import Pin

# Enable pin
LCD_E  = Pin(26, Pin.OUT)
LCD_E.off()
# Register Select pin, 1 - data, 0 - command
LCD_RS = Pin(27, Pin.OUT)

# Four bit data pins
dataPins = (18, 19, 20, 21)

# Empty list for data pin objects
LCD_D = []
# Construct the list of data pin objects
for p in dataPins:
    LCD_D.append(Pin(p, Pin.OUT))

def lcd_set_data_bits(data):
    """Set the eight data pins according to parameter data"""
    for i in range(0, 4):
        # For each pin set the value according to the corresponding bit
        LCD_D[i].value(data & (1 << (i + 4)))

def lcd_write_nibble(data):
    """Write the upper nibble of the data byte"""
    lcd_set_data_bits(data)
    LCD_E.on()
    time.sleep_us(1)
    LCD_E.off()

def lcd_write_byte(data):
    """Write a byte of data to the LCD controller"""
    lcd_write_nibble(data)       # write upper nibble
    lcd_write_nibble(data << 4)  # write lower nibble

def lcd_command(data):
    """write a command to the LCD controller"""
    # RS pin = 0, write to command register
    LCD_RS.off()
    # Write the command
    lcd_write_byte(data)
    time.sleep_ms(2)

def lcd_data(data):
    """Write data to the LCD controller"""
    # RS pin = 1, write to data register
    LCD_RS.on()
    # Write the data
    lcd_write_byte(data)

def lcd_init():
    """Initialization sequence of HD44780"""
    LCD_RS.off()     # These are all commands
    time.sleep_ms(20)
    lcd_write_nibble(0x30)
    time.sleep_ms(5)
    lcd_write_nibble(0x30)
    time.sleep_ms(1)
    lcd_write_nibble(0x30)
    time.sleep_ms(1)
    lcd_write_nibble(0x20)
    time.sleep_ms(1)
    lcd_command(0x28)    # 4-bit, 2 lines, 5x7 pixels
    lcd_command(0x06)    # increment, no shift
    lcd_command(0x01)    # clear display
    lcd_command(0x0F)    # display on, curson on and blinking

def lcd_put_string(s):
    """Display a character string on the LCD"""
    for c in s:
        lcd_data(ord(c))

def lcd_cursor(line, column):
    """Move the cursor to a specified location of the display"""
    if line == 1:
        cmd = 0x80
    elif line == 2:
        cmd = 0xC0
    else:
        return

    if column < 1 or column > 20:
        return

    cmd += column - 1

    lcd_command(cmd)

# Send initialization sequence
lcd_init()

# Infinite loop to blink "Hello" on the LCD
while True:
    # Write "Temperature" on line one
    lcd_cursor(1, 3)       # move cursor to line 1, column 4
    lcd_put_string('Temperature')
    # Write the temperature value on line two
    TEMP = 89.75           # a number for temperature
    TEMP_STR = str(TEMP)   # convert temperature to a string
    TEMP_STR = TEMP_STR + chr(223) + 'F'  # append degree F
    lcd_cursor(2, 5)       # move cursor to line 2, column 8
    lcd_put_string(TEMP_STR) # send the string to the LCD
    time.sleep_ms(1000)    # wait for 1 second
    lcd_command(1)         # clear display
    time.sleep_ms(1000)    # wait for 1 second then repeat

"""Program 3-1: Blink message "Hello" using 8-bit data mode"""

import time
from machine import Pin

# Read/Write pin, 1 - read, 0 - write
LCD_RW = Pin(28, Pin.OUT)
LCD_RW.off()

# Enable pin
LCD_E = Pin(26, Pin.OUT)
LCD_E.off()

# Register Select pin, 1 - data, 0 - command
LCD_RS = Pin(27, Pin.OUT)

# Eight bit data pins
dataPins = (14, 15, 16, 17, 18, 19, 20, 21)

# Empty list for data pin objects
LCD_D = []
# Construct the list of data pin objects
for pn in dataPins:
    LCD_D.append(Pin(pn, Pin.OUT))


def lcd_ready():
    """Wait until the LCD is ready"""
    # Make data pins input
    for p in LCD_D:
        p.init(Pin.IN)
    # RS = 0, read status register. when RS = 0 select command register
    LCD_RS.off()
    # RW = 1, read data pins  when RW = 1 select read mode
    LCD_RW.on()

    # Loop until busy bit is 0
    while True:
        LCD_E.on()
        busy = LCD_D[7].value()
        LCD_E.off()
        if busy == 0:
            break

    # RW = 0, write data pins
    LCD_RW.off()
    # Restore data pins to output
    for p in LCD_D:
        p.init(Pin.OUT)


def lcd_set_data_bits(data):
    """Set the eight data pins according to parameter data"""
    for i in range(0, 8):
        # For each pin set the value according to the corresponding bit
        LCD_D[i].value(data & (1 << i))


def lcd_write_byte(data):
    """Write a byte of data to the LCD controller"""
    # Set the data bits
    lcd_set_data_bits(data)
    # Pulse the Enable pin
    LCD_E.on()
    time.sleep_us(1)
    LCD_E.off()


def lcd_command(data):
    """write a command to the LCD controller"""
    # Wait until the LCD controller is ready
    lcd_ready()
    # RS pin = 0, write to command register
    LCD_RS.off()
    # Write the command
    lcd_write_byte(data)


def lcd_data(data):
    """Write data to the LCD controller"""
    # Wait until the LCD controller is ready
    lcd_ready()
    # RS pin = 1, write to data register
    LCD_RS.on()
    # Write the data
    lcd_write_byte(data)


# Initialization sequence of HD44780
def lcd_init():
    """Initialization sequence of HD44780"""
    LCD_RS.off()  # These are all commands
    time.sleep_ms(20)
    lcd_write_byte(0x30)
    time.sleep_ms(5)
    lcd_write_byte(0x30)
    time.sleep_ms(1)
    lcd_write_byte(0x30)
    time.sleep_ms(1)
    lcd_command(0x38)  # 8-bit, 2 lines, 5x7 pixels
    lcd_command(0x06)  # increment, no shift
    lcd_command(0x01)  # clear display
    lcd_command(0x0F)  # display on, curson on and blinking


# Send initialization sequence
lcd_init()

# Infinite loop to blink "Hello" on the LCD
while True:
    # Write "Hello" on the LCD
    lcd_data(ord('H'))
    lcd_data(ord('e'))
    lcd_data(ord('l'))
    lcd_data(ord('l'))
    lcd_data(ord('o'))
    time.sleep_ms(1000)  # wait for 1 second
    lcd_command(1)  # clear display
    time.sleep_ms(1000)  # wait for 1 second then repeat

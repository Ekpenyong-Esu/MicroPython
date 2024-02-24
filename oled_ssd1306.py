""" Program 12-1: OLED_SSD1306 via I2C
    This program communicates with the OLED_SSD1306 via I2C.
    It writes "ABC" on the display and fills the rest of the
    display with a checkerboard pattern.
    Connection: SCL - GP17, SDA - GP16
"""

import time
from machine import I2C, Pin

DEV_ADDR = 0x3C
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
SCREEN_PAGE_NUM = 8

# Instantiate i2c, SCL - GP17, SDA - GP16
i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq = 400_000)

def ssd1306_data(data):
    """Write a byte of data to SSD1306"""
    i2c.writeto(DEV_ADDR, bytearray([0xC0, data]))

def ssd1306_command(cmd):
    """Write a byte of command to SSD1306"""
    i2c.writeto(DEV_ADDR, bytearray([0x80, cmd]))

def ssd1306_init():
    # Initialize SSD1306
    INIT_SEQ = (
        0xae,       # turn off oled panel
        0x00,       # set low column address
        0x10,       # set high column address
        0x40,       # set start line address
        0x20, 0x02, # page addressing mode
        0xc8,       # top-down segment (4th quadrant)
        0x81,       # set contrast control register
        0xcf, 0xa1, # set segment re-map 95 to 0
        0xa6,       # set normal display
        0xa8,       # set multiplex ratio(1 to 64)
        0x3f,       # 1/64 duty
        0xd3,       # set display offset
        0x00,       # not offset
        0xd5,       # set display clock divide ratio/oscillator frequency
        0x80,       # set divide ratio
        0xd9,       # set pre-charge period
        0xf1, 0xda, # set com pins hardware configuration
        0x12, 0xdb, # set vcomh
        0x40, 0x8d, # set Charge Pump enable/disable
        0x14,       # set(0x10) disable
        0xaf        # turn on oled panel
        )

    time.sleep_ms(100)

    for command in INIT_SEQ:
        ssd1306_command(command)


def ssd1306_setRegion(x0, x1, y):
    """Set active region to x0, x1, y, y.
       The maximum region can be set is a page."""
    ssd1306_command(0x21)       # set column
    ssd1306_command(x0)         # starting column
    ssd1306_command(x1)         # end column
    ssd1306_command(0x22)       # set page
    ssd1306_command(y)          # starting page
    ssd1306_command(y)          # end page


ssd1306_init()

# Sample font table
FONT_TABLE = (
    (0x7e, 0x11, 0x11, 0x11, 0x7e, 0),  # A
    (0x7f, 0x49, 0x49, 0x49, 0x36, 0),  # B
    (0x3e, 0x41, 0x41, 0x41, 0x22, 0))  # C

# Write ABC at the beginning of first line
ssd1306_setRegion(0, SCREEN_WIDTH - 1, 0)
for j in range(3):
    for i in range(6):
        ssd1306_data(FONT_TABLE[j][i])

# Clear the remaining part of the line
for i in range(SCREEN_WIDTH - 3 * 6):
    ssd1306_data(0)

# For the rest of the lines
for page in range(1, SCREEN_PAGE_NUM):
    ssd1306_setRegion(0, SCREEN_WIDTH - 1, page)

    # Fill with checker board pattern
    for j in range(int(SCREEN_WIDTH / 8)):
        for k in range(4):
            ssd1306_data(0xF0)

        for k in range(4):
            ssd1306_data(0x0F)

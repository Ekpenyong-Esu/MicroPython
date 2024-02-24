import utime
from machine import Pin

# Define LCD pin configuration
RS_PIN = 0  # Register select
EN_PIN = 1  # Enable
D4_PIN = 2  # Data bit 4
D5_PIN = 3  # Data bit 5
D6_PIN = 4  # Data bit 6
D7_PIN = 5  # Data bit 7

# Define LCD commands
LCD_CLEAR = 0x01
LCD_HOME = 0x02
LCD_ENTRY_MODE = 0x04
LCD_DISPLAY_CONTROL = 0x08
LCD_FUNCTION_SET = 0x20
LCD_SET_CGRAM_ADDR = 0x40
LCD_SET_DDRAM_ADDR = 0x80

# Define LCD entry mode flags
LCD_ENTRY_RIGHT = 0x00
LCD_ENTRY_LEFT = 0x02
LCD_ENTRY_SHIFT_INCREMENT = 0x01
LCD_ENTRY_SHIFT_DECREMENT = 0x00

# Define LCD display control flags
LCD_DISPLAY_ON = 0x04
LCD_DISPLAY_OFF = 0x00
LCD_CURSOR_ON = 0x02
LCD_CURSOR_OFF = 0x00
LCD_BLINK_ON = 0x01
LCD_BLINK_OFF = 0x00

# Define LCD function set flags
LCD_8BIT_MODE = 0x10
LCD_4BIT_MODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10_DOTS = 0x04
LCD_5x8_DOTS = 0x00

class LCD:
    def __init__(self, rs, en, d4, d5, d6, d7):
        self.rs = Pin(rs, Pin.OUT)
        self.en = Pin(en, Pin.OUT)
        self.d4 = Pin(d4, Pin.OUT)
        self.d5 = Pin(d5, Pin.OUT)
        self.d6 = Pin(d6, Pin.OUT)
        self.d7 = Pin(d7, Pin.OUT)

        self.setup()

    def setup(self):
        self.send_command(0x33)  # Initialization
        self.send_command(0x32)  # Initialization
        self.send_command(LCD_FUNCTION_SET | LCD_4BIT_MODE | LCD_2LINE | LCD_5x8_DOTS)
        self.send_command(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON)
        self.send_command(LCD_CLEAR)
        self.send_command(LCD_ENTRY_MODE | LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT)

    def send_command(self, command):
        self.rs.value(0)
        self.write_4bits(command >> 4)
        self.write_4bits(command & 0x0F)

    def write_data(self, data):
        self.rs.value(1)
        self.write_4bits(data >> 4)
        self.write_4bits(data & 0x0F)

    def write_4bits(self, value):
        self.d7.value((value >> 3) & 1)
        self.d6.value((value >> 2) & 1)
        self.d5.value((value >> 1) & 1)
        self.d4.value(value & 1)
        self.pulse_enable()

    def pulse_enable(self):
        self.en.value(0)
        utime.sleep_us(1)
        self.en.value(1)
        utime.sleep_us(1)
        self.en.value(0)
        utime.sleep_us(100)

    def clear(self):
        self.send_command(LCD_CLEAR)
        utime.sleep_ms(2)

    def home(self):
        self.send_command(LCD_HOME)
        utime.sleep_ms(2)

    def set_cursor(self, col, row):
        offsets = [0x00, 0x40, 0x14, 0x54]
        self.send_command(LCD_SET_DDRAM_ADDR | (col + offsets[row]))

    def print(self, text):
        for char in text:
            self.write_data(ord(char))

# Example usage
lcd = LCD(RS_PIN, EN_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN)
lcd.clear()
lcd.print("Hello, World!")
lcd.set_cursor(0, 1)
lcd.print("MicroPython")

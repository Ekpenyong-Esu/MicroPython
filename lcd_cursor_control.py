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
        self.data_pins = [Pin(pin, Pin.OUT) for pin in [d4, d5, d6, d7]]

        self.setup()

    def setup(self):
        self.send_nibble(0x03)
        utime.sleep_ms(4)
        self.send_nibble(0x03)
        utime.sleep_ms(4)
        self.send_nibble(0x03)
        utime.sleep_ms(4)
        self.send_nibble(0x02)  # Set 4-bit mode
        self.send_command(LCD_FUNCTION_SET | LCD_4BIT_MODE | LCD_2LINE | LCD_5x8_DOTS)
        self.send_command(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON)
        self.send_command(LCD_CLEAR)
        self.send_command(LCD_ENTRY_MODE | LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT)

    def send_command(self, command):
        self.rs.value(0)
        self.send_byte(command)

    def send_data(self, data):
        self.rs.value(1)
        self.send_byte(data)

    def send_nibble(self, nibble):
        for i in range(4):
            self.data_pins[i].value((nibble >> i) & 1)
        self.pulse_enable()

    def send_byte(self, value):
        self.send_nibble(value >> 4)
        self.send_nibble(value & 0x0F)

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

    def send_text(self, text):
        for char in text:
            self.send_data(ord(char))

    def print_number(self, number):
        self.clear()
        self.send_text(str(number))
        utime.sleep_ms(500)
        self.clear()
        utime.sleep_ms(500)

    def display_cursor(self, show_cursor=True):
        if show_cursor:
            self.send_command(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON | LCD_CURSOR_ON)
        else:
            self.send_command(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON | LCD_CURSOR_OFF)

# Example usage for cursor control
lcd = LCD(RS_PIN, EN_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN)

try:
    lcd.display_cursor(False)  # Turn off the cursor initially

    while True:
        lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.send_text("Cursor: On")
        lcd.display_cursor(True)
        utime.sleep_ms(2000)

        lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.send_text("Cursor: Off")
        lcd.display_cursor(False)
        utime.sleep_ms(2000)

except KeyboardInterrupt:
    pass
finally:
    lcd.clear()

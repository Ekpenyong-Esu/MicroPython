import machine
import time

i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))

i2c.writeto(0x27, bytes([0x33, 0x32, 0x28]))  # Initialize
i2c.writeto(0x27, bytes([0x0C, 0x01]))  # Turn on LCD
i2c.writeto(0x27, bytes([0x06, 0x0F]))  # Set cursor mode
i2c.writeto(0x27, bytes([0x01]))  # Clear display

while True:
    i2c.writeto(0x27, bytes([0x80]))  # Set cursor to first line
    i2c.writeto(0x27, bytes("Hello World!"))
    time.sleep(2)

    i2c.writeto(0x27, bytes([0xC0]))  # Set cursor to second line
    i2c.writeto(0x27, bytes("MicroPython"))
    time.sleep(2)

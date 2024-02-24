from machine import Pin, SPI
import time

# Define EEPROM opcodes
EEPROM_READ = 0b00000011
EEPROM_WRITE = 0b00000010
EEPROM_WREN = 0b00000110
EEPROM_WRDI = 0b00000100

# Initialize SPI
spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# Define Chip Select Pin
cs = Pin(5, Pin.OUT)

# Function to enable write operations
def enable_write():
    cs.value(0)
    spi.write(bytearray([EEPROM_WREN]))
    cs.value(1)
    time.sleep_ms(10)

# Function to write data to EEPROM
def write_eeprom(addr, data):
    enable_write()
    cs.value(0)
    spi.write(bytearray([EEPROM_WRITE, (addr >> 8) & 0xFF, addr & 0xFF]) + data)
    cs.value(1)
    time.sleep_ms(10)

# Function to read data from EEPROM
def read_eeprom(addr, length):
    cs.value(0)
    spi.write(bytearray([EEPROM_READ, (addr >> 8) & 0xFF, addr & 0xFF]))
    data = spi.read(length)
    cs.value(1)
    return data

# Example usage
# Write data to EEPROM
write_eeprom(0, b'Hello')

# Read data from EEPROM
data = read_eeprom(0, 5)
print("Data read from EEPROM:", data.decode('utf-8'))

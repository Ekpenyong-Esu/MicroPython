from machine import Pin, I2C
import time

# Define I2C address of the EEPROM
EEPROM_ADDR = 0b1010000

# Initialize I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Function to write data to EEPROM
def write_eeprom(addr, data):
    i2c.writeto_mem(EEPROM_ADDR, addr, data)

# Example usage
# Write data to EEPROM starting from address 0
write_eeprom(0, b'Hello')

print("Data written to EEPROM")

# Optional: Read data from EEPROM to verify
data_read = i2c.readfrom_mem(EEPROM_ADDR, 0, 5)
print("Data read from EEPROM:", data_read.decode('utf-8'))

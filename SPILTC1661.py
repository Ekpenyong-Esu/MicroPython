import machine
import utime

# LTC1661 Configuration
SCK_PIN = 2  # Replace with your GPIO pin
SDI_PIN = 3  # Replace with your GPIO pin
CS_PIN = 5   # Replace with your GPIO pin

# Configure SPI for LTC1661
spi = machine.SPI(0, baudrate=1000000, polarity=0, phase=0, sck=SCK_PIN, mosi=SDI_PIN)

# Configure Chip Select (CS) pin
cs_pin = machine.Pin(CS_PIN, machine.Pin.OUT)

# Function to send data to LTC1661
def send_to_dac(value):
    cs_pin.value(0)  # Activate CS
    spi.write(bytes([value >> 8, value & 0xFF]))
    cs_pin.value(1)  # Deactivate CS

# Generate sawtooth waveform
def generate_sawtooth():
    for i in range(4096):  # 12-bit resolution of LTC1661
        send_to_dac(i)
        utime.sleep_us(10)  # Adjust delay based on your requirements

# Run the sawtooth waveform generation
generate_sawtooth()

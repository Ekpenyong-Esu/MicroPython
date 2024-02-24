import machine
import utime

# Define SPI pins (replace these with the actual GPIO pin numbers)
spi = machine.SPI(0, baudrate=1000000, polarity=0, phase=0, sck=2, mosi=3, miso=4)

# Define your SPI device's CS (Chip Select) pin
cs_pin = machine.Pin(5, machine.Pin.OUT)

def read_spi_data():
    cs_pin.value(0)  # Activate the CS pin

    # Send data to SPI device (replace b'\x01' with your actual data)
    spi.write(b'\x01')

    # Read data from SPI device
    received_data = spi.read(1)

    cs_pin.value(1)  # Deactivate the CS pin

    return received_data

while True:
    data = read_spi_data()
    print("Received data:", data)

    utime.sleep(1)

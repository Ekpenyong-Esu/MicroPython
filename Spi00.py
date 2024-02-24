import machine
import ustruct

# SPI pins
SCK = machine.Pin(2)  
MOSI = machine.Pin(3)
MISO = machine.Pin(4)
CS = machine.Pin(5)

# Create SPI object
spi = machine.SPI(0, baudrate=1000000, polarity=1, phase=1, sck=SCK, mosi=MOSI, miso=MISO)

# EEPROM commands
WREN = 0x06        # Set write enable latch
WRDI = 0x04        # Reset write enable latch
RDSR = 0x05        # Read status register
WRSR = 0x01        # Write status register
READ = 0x03        # Read memory
WRITE = 0x02       # Write memory

# Initialize CS pin 
CS.init(CS.OUT, value=1)   

def wr_en():
    CS.value(0)
    spi.write(bytearray([WREN]))
    CS.value(1)

def wr_dis():
    CS.value(0)
    spi.write(bytearray([WRDI]))
    CS.value(1)
    
def read_status():
    CS.value(0)
    spi.write(bytearray([RDSR]))
    status = ustruct.unpack('<B', spi.read(1))[0]
    CS.value(1)
    return status

def write_status(status):
    CS.value(0)
    spi.write(bytearray([WRSR, status]))
    CS.value(1)
    
def read_mem(addr, length):
    CS.value(0)
    spi.write(bytearray([READ, (addr>>8)&0xFF, addr&0xFF]))
    data = spi.read(length)
    CS.value(1)
    return data

def write_mem(addr, data):
    CS.value(0)
    spi.write(bytearray([WRITE, (addr>>8)&0xFF, addr&0xFF]))
    spi.write(data)
    CS.value(1)

# Example usage
wr_en()
write_status(0) # Clear status register
wr_dis()

data = b'Hello World'
write_mem(0, data) 
rd = read_mem(0, len(data))
print(rd)
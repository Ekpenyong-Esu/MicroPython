"""Program 8-3  Read 25AA010A EEPROM through SPI
   Connections: SCK - GP10, MOSI - GP11, MISO - GP12, CS - GP13
"""

from machine import SPI, Pin

MEMORY_SIZE = 128
READ_CODE = 3

# Instantiate SPI1
spi = SPI(1, sck = Pin(10), mosi = Pin(11), miso = Pin(12), baudrate = 2_000_000, bits = 8,
           polarity = 1, phase = 1, firstbit = SPI.MSB)


ncs = Pin(13, Pin.OUT)      # assign GP13 for chip select
ncs.value(1)                # chip select is active low and idle high

def read_bytes(addr, nbytes):
    """function to read n bytes from a starting address"""
    if addr + nbytes > MEMORY_SIZE:    # boundary check
        print('Warning: read beyond end of memory')
    buf = bytearray(nbytes) # create a buffer to hold n bytes
    cmd = bytearray([READ_CODE, addr]) # create a read command
    ncs.value(0)            # assert chip select
    spi.write(cmd)          # send read command
    spi.readinto(buf, 0)    # read data into buffer
    ncs.value(1)            # deassert chip select
    return buf              # return buffer

# Read 16 bytes starting from 0x24
da = read_bytes(0x24, 16)
print(len(da), 'bytes read')
for d in da:
    print(hex(d), end = ' ')   # print out the data read

"""Program 8-4  Write 25AA010A EEPROM through SPI
   Connections: SCK - GP10, MOSI - GP11, MISO - GP12, CS - GP13
"""

from machine import SPI, Pin

MEMORY_SIZE = 128
PAGE_SIZE = 16
READ_CODE = 3
WRITE_CODE = 2
WREN_CODE = 6
RDSR_CODE = 5

# Instantiate SPI1 with its parameters
spi = SPI(1, sck = Pin(10), mosi = Pin(11), miso = Pin(12),
           baudrate = 2_000_000, bits = 8, polarity = 0, 
           phase = 0, firstbit = SPI.MSB)
ncs = Pin(13, Pin.OUT)      # assign GP13 as chip select
ncs.value(1)                # chip select is active low and idle high

def read(addr, nbytes):
    """Function to read n bytes from a starting address"""
    if addr + nbytes > MEMORY_SIZE:  # boundary check
        print('Warning: read beyond end of memory')
    buf = bytearray(nbytes) # create a buffer to hold n bytes
    cmd = bytearray([READ_CODE, addr])  # create read command
    ncs.value(0)            # assert chip select
    spi.write(cmd)          # send read command
    spi.readinto(buf, 0)    # read data into buffer
    ncs.value(1)            # deassert chip select
    return buf              # return the buffer with data read


def status():
    """Read the Status Register and return the content"""
    cmd = bytearray([RDSR_CODE]) # read status command
    ncs.value(0)            # assert chip select
    spi.write(cmd)          # send read status command
    sreg = spi.read(1, 0)   # read status register
    ncs.value(1)            # deassert chip select
    return sreg[0]          # return status

def wip():
    """Check to see whether the write is in progress
       Return True if WIP bit is set.
    """
    if status() & 1:        # WIP bit is bit 0
        return True
    return False

def write_page(addr, data):
    """Write data bytes starting at addr
       The data is expected to be a list and will be converted to a bytearray.
       No page boundary is checked. If data exceeds the end of the page,
       it will overwrite the beginning of the page.
    """
    if addr % PAGE_SIZE + len(data) > PAGE_SIZE:
        print('Warning: write beyond end of the page')
    cmd = bytearray([WREN_CODE])
    ncs.value(0)            # assert chip select
    spi.write(cmd)          # write enable command
    ncs.value(1)            # deassert chip select
    # Build the write command with data in a list
    cmdlist = [WRITE_CODE]
    cmdlist.append(addr)
    for dbyte in data:
        cmdlist.append(dbyte)
    cmd = bytearray(cmdlist) # convert the list to a bytearray

    ncs.value(0)            # assert chip select
    spi.write(cmd)          # send the write command through SPI
    ncs.value(1)            # deassert chip select

    while wip():            # wait for write to finish
        print('.', end = '')
    print()                 # print a newline


def dump_memory():
    """Dump the memory of the whole device"""
    for addr in range(0x00, 0x80, 0x10):     # for 8 lines of 16 bytes per line
        print(f'{addr:02x}:', end = ' ')     # print the starting address
        d16 = read(addr, 16)                 # read 16 bytes
        for index, data in enumerate(d16):
            print(f'{data:02x}', end = ' ')  # print out the data
            if index == 7:
                print(' ', end = ' ')        # print an extra space
        print('')                            # print a newline

dump_memory()               # dump the memory before write

# Write a page of data
START_AT = 0x30
data_list = []                  # start with an empty list
for i in range(0x47, 0x57):     # fill the list with 16 data bytes
    data_list.append(i)
write_page(START_AT, data_list) # write the data to the memory

dump_memory()                   # dump the memory after write

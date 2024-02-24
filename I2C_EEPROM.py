"""Program 9-6  Write data to a 24AA01 EEPROM through I2C
   Connections: SCL - GP17, SDA - GP16.
"""

from machine import I2C, Pin

MEMORY_SIZE = 128
PAGE_SIZE = 8
DEV_ADDR = 80

# Instantiate i2c
i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq = 400_000)


def read(addr, nbytes):
    """Function to read n bytes from a starting address"""
    if addr + nbytes > MEMORY_SIZE:  # boundary check
        print('Warning: read beyond end of memory')
    buf = i2c.readfrom_mem(DEV_ADDR, addr, nbytes, addrsize=8)
    return buf             # return the buffer with data read


def acknowledge_polling():
    """Polling the device until the programming is done"""
    while True:
        try:             # execute next statement and anticipate an error
            i2c.writevto(DEV_ADDR, ())
        except OSError:  # if OSError encountered
            print('.', end = '')
        else:            # if no OSError
            print()      # print a newline
            break


def write_page(addr, data):
    """Write data bytes starting at addr.
       The data is expected to be a list and will be converted to
       a bytearray.  No page boundary is checked. If data exceeds
       the end of the page, it will overwrite the beginning of the page.
    """
    if addr % PAGE_SIZE + len(data) > PAGE_SIZE:
        print('Warning: write beyond end of the page')

    i2c.writeto_mem(DEV_ADDR, addr, bytearray(data), addrsize=8)
    acknowledge_polling()   # wait until the programming is done


def dump_memory():
    """Dump the memory of the whole device"""
    for addr in range(0x00, 0x80, 0x10):    # for 8 lines of 16 bytes per line
        print(f'{addr:02x}:', end = ' ')    # print the starting address
        d16 = read(addr, 16)                # read 16 bytes
        for index, data in enumerate(d16):
            print(f'{data:02x}', end = ' ') # print out the data
            if index == 7:
                print(' ', end = ' ')       # print an extra space
        print('')                           # print a newline


dump_memory()                  # dump the memory before write

# Write a page of data
START = 0x30                   # starting address
data_list = []                 # start with an empty list
for i in range(0, 8):          # fill the list with 8 data bytes
    data_list.append(0x55)
write_page(START, data_list)   # write the data to the memory

dump_memory()                  # dump the memory after write

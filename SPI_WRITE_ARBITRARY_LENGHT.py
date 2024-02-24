"""Program 8-6  Write Arbitrary Length of data to a 25AA010A EEPROM through SPI
   Connections: SCK - GP10, MOSI - GP11, MISO - GP12, CS - GP13
   Define a class for the EEPROM
"""

from machine import SPI, Pin

class SpiEEPROM1k:
    """A 1 kb serial EEPROM on SPI"""
    MEMORY_SIZE = 128
    READ_CODE = 3
    WRITE_CODE = 2
    WREN_CODE = 6
    RDSR_CODE = 5
    PAGE_SIZE = 16

    def __init__(self, id_, pins, params):
        # pins = sck, mosi, miso, ncs
        # params =  baud, bits, pol, pha, firstbit
        # Set SPI pin assignements
        self.spi = SPI(id_, sck = Pin(pins[0]), baudrate = params[0], bits = params[1],
                      polarity = params[2], phase = params[3], firstbit = params[4],
                        mosi = Pin(pins[1]), miso = Pin(pins[2]))

        self.ncs = Pin(pins[3], Pin.OUT) # assign GP13 as chip select
        self.ncs.value(1)                # chip select is idle high

    def read(self, addr, nbytes):
        """Function to read n bytes from a starting address"""
        if addr + nbytes > self.MEMORY_SIZE:     # boundary check
            print('Warning: read beyond end of memory')
        buf = bytearray(nbytes)     # create a buffer to hold n bytes
        cmd = bytearray([self.READ_CODE, addr])  # create read command
        self.ncs.value(0)           # assert chip select
        self.spi.write(cmd)         # send READ instruction and starting addr.
        self.spi.readinto(buf, 0)   # read data into buffer
        self.ncs.value(1)           # deassert chip select
        return buf                  # return the buffer with data read

    def status(self):
        """Read the Status Register and return the content"""
        cmd = bytearray([self.RDSR_CODE]) # read status command
        self.ncs.value(0)           # assert chip select
        self.spi.write(cmd)         # issue read status command
        sreg = self.spi.read(1, 0)  # read status register
        self.ncs.value(1)           # deassert chip select
        return sreg[0]              # return status

    def wip(self):
        """Check to see whether the write is in progress.
           Return True if WIP bit is set.
        """
        if self.status() & 1:
            return True
        return False

    def write_page(self, addr, data):
        """Write data bytes starting at addr.
           The data is expected to be a list and will be converted to 
           a bytearray.
           No page boundary is checked. If data exceeds the end of the page,
           it will overwrite the beginning of the page.
        """
        if self.status() & 0xC0:
            print('Warning: Memory may be protected.')
        cmd = bytearray([self.WREN_CODE])
        self.ncs.value(0)           # assert chip select
        self.spi.write(cmd)         # send write enable command
        self.ncs.value(1)           # deassert chip select
        # Build the write command
        cmdlist = [self.WRITE_CODE]
        cmdlist.append(addr)
        for dbyte in data:
            cmdlist.append(dbyte)
        cmd = bytearray(cmdlist)
        # Send the write command through SPI
        self.ncs.value(0)           # assert chip select
        self.spi.write(cmd)
        self.ncs.value(1)           # deassert chip select
        # Wait for write to finish
        while self.wip():
            print('.', end = '')
        print('')

    def write(self, addr, data):
        """Write to memory that may cross the page boundary"""
        starting_addr = addr   # starting address for the page
        da = []                # start with a blank data array
        for d in data:
            da.append(d)       # fill the array with data
            addr += 1
            if (addr % self.PAGE_SIZE) == 0:   # when the page is full
                self.write_page(starting_addr, da)
                starting_addr = addr           # prepare for next page
                da = []
                if (addr >= self.MEMORY_SIZE): # reach the end of the memory
                    break
        if len(da) > 0:        # wrap up the remaining data
            self.write_page(starting_addr, da)


# Instantiate an object of eeprom
SPI_ID = 1
PIN_ASSIGNMENTS = (10, 11, 12, 13)         # sck, mosi, miso, ncs
SPI_PAREMS = (2_000_000, 8, 0, 0, SPI.MSB) # baud, bits, pol, pha, firstbit
eeprom = SpiEEPROM1k(SPI_ID, PIN_ASSIGNMENTS, SPI_PAREMS)


def dump_memory():
    """Dump the memory of the whole device"""
    for addr in range(0x00, 0x80, 0x10):     # for 8 lines of 16 bytes per line
        print(f'{addr:02x}:', end = ' ')     # print the starting address
        d16 = eeprom.read(addr, 16)          # read 16 bytes
        for index, data in enumerate(d16):
            print(f'{data:02x}', end = ' ')  # print out the data
            if index == 7:
                print(' ', end = ' ')        # print an extra space
        print('')                            # print a newline

dump_memory()                  # dump the memory before write

# Write a page of data
data_list = []                 # start with an empty list
START = 0x20                   # starting address
for i in range(0, 16):         # fill the list with 16 data bytes
    data_list.append(i + START)
eeprom.write_page(START, data_list) # write the data starting at 0x20

dump_memory()                  # dump the memory after write

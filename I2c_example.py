"""Program 9-7  Write data to a 24AA01 EEPROM through I2C
   Connections: SCL - GP17, SDA - GP16.
   Define a class for the EEPROM. Allow writing across a page boundary.
"""

from machine import I2C, Pin

class I2cEEPROM1k:
    """A 1 kb serial EEPROM on I2C"""
    MEMORY_SIZE = 128
    PAGE_SIZE = 8

    def __init__(self, id_, addr, pins, freq):
        # Instantiate i2c
        self.i2c = I2C(id_, scl = Pin(pins[0]),
                           sda = Pin(pins[1]), freq = freq)
        self.dev_addr = addr

    def read(self, addr, nbytes):
        """Function to read n bytes from a starting address"""
        if addr + nbytes > self.MEMORY_SIZE:  # boundary check
            print('Warning: read beyond end of memory')
        buf = self.i2c.readfrom_mem(self.dev_addr, addr, nbytes, addrsize=8)
        return buf             # return the buffer with data read


    def acknowledge_polling(self):
        """Polling the device until the programming is done"""
        while True:
            try:             # execute next statement and anticipate an error
                self.i2c.writevto(self.dev_addr, ())
            except OSError:  # if OSError encountered
                print('.', end = '')
            else:            # if no OSError
                print()      # print a newline
                break

    def write_page(self, addr, data):
        """Write data bytes starting at addr.
           The data is expected to be a list and will be converted to
           a bytearray.  No page boundary is checked. If data exceeds
           the end of the page, it will overwrite the beginning of the page.
        """
        self.i2c.writeto_mem(self.dev_addr, addr, bytearray(data), addrsize=8)
        self.acknowledge_polling()   # wait until the programming is done

    def write(self, addr, data):
        """Page the memory write"""
        starting_addr = addr      # starting address for the page
        darray = []               # start with a blank data array
        for dbyte in data:
            darray.append(dbyte)  # fill the array with data
            addr += 1
            if addr % self.PAGE_SIZE == 0:   # when the page is full
                self.write_page(starting_addr, darray)
                starting_addr = addr         # prepare for next page
                darray = []
                if addr >= self.MEMORY_SIZE: # reach the end of the memory
                    break
        if len(darray) > 0:                  # wrap up the remaining data
            self.write_page(starting_addr, darray)


# Constructor parameters: id, dev_addr, (scl pin, sda pin), frequency
eeprom = I2cEEPROM1k(0, 80, (17, 16), 400_000)

def dump_memory():
    """Dump the memory of the whole device"""
    for addr in range(0x00, 0x80, 0x10):    # for 8 lines of 16 bytes per line
        print(f'{addr:02x}:', end = ' ')    # print the starting address
        d16 = eeprom.read(addr, 16)         # read 16 bytes
        for index, data in enumerate(d16):
            print(f'{data:02x}', end = ' ') # print out the data
            if index == 7:
                print(' ', end = ' ')       # print an extra space
        print('')                           # print a newline

dump_memory()                  # dump the memory before write

# Write a page of data
data_list = []                 # start with an empty list
START = 0x25                   # starting address
for i in range(0, 32):         # fill the list with 32 data bytes
    data_list.append(0x55)
eeprom.write(START, data_list) # write the data to the memory

dump_memory()                  # dump the memory after write

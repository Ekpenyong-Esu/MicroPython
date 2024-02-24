"""Program 8-1: Using LTC1661 DAC to generate a sawtooth waveform
   LTC1661 is connected to the Pico board by SPI.
   The connections are: SCK - GP18, MOSI - GP19, CS - GP21.
"""

from machine import SPI, Pin

# Instantiate SPI0, assign pins, and set parameters
spi = SPI(0, sck = Pin(18), mosi = Pin(19), baudrate = 2_000_000,
          bits = 8, polarity = 0, phase = 0, firstbit = SPI.MSB)

ncs = Pin(17, Pin.OUT)     # assign GP21 for chip select
ncs.value(1)               # chip select is active low and idle high

n = 0
while True:
    msb = 0x90 + (n >> 6)  # high byte is command + upper 4 bits of data
    lsb = (n << 2) & 0xFC  # low byte is lower 6 bits of data left justified
    data = bytearray([msb, lsb])  # construct the bytearray for output
    ncs.value(0)           # assert chip select
    spi.write(data)        # write the data through SPI
    ncs.value(1)           # deassert chip select
    n += 1
    n &= 0x3FF             # keep it to 10-bit

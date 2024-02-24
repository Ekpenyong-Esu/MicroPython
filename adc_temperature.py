import machine
import utime

#  The ADC is configured to read from ADC channel 4, which is connected to the 
# built-in temperature sensor on the Raspberry Pi Pico.
sensor_temp = machine.ADC(4)

# The Pico's ADC produces readings between 0 and 65535, which are then scaled to 0-3.3V
conversion_factor = 3.3 / (65535)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    utime.sleep(2)
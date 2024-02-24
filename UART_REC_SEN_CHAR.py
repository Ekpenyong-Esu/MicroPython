import machine
import utime

# Define UART parameters
uart_port = 0  # UART0 on the Raspberry Pi Pico
baud_rate = 9600

# Initialize UART
uart = machine.UART(uart_port, baud_rate,  rx = machine.Pin(1), tx = machine.Pin(0))

while True:
    # Check if there is any data available to read
    if uart.any():
        # Read a single character
        received_char = uart.read(1)
        
        # Print the received character
        print("Received char:", received_char.decode('utf-8'))
        
        # Send a character back
        uart.write(received_char)

    # Add a small delay to avoid busy waiting
    utime.sleep_ms(10)

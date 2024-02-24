import machine
import utime

# Define UART parameters
uart_port = 0  # UART0 on the Raspberry Pi Pico
baud_rate = 9600

# Initialize UART
uart = machine.UART(uart_port, baud_rate)

while True:
    # Check if there is any data available to read
    if uart.any():
        # Read a string (assuming the string is terminated by a newline character)
        received_string = uart.readline()
        
        # Print the received string
        print("Received string:", received_string.decode('utf-8'))
        
        # Send a string back
        uart.write(received_string)

    # Add a small delay to avoid busy waiting
    utime.sleep_ms(10)

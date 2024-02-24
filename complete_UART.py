import machine
import utime
import struct

# Define UART parameters
uart_port = 0  # UART0 on the Raspberry Pi Pico
baud_rate = 9600

# Initialize UART
uart = machine.UART(uart_port, baud_rate)

def receive_char():
    if uart.any():
        received_char = uart.read(1)
        return received_char.decode('utf-8')
    return None

def send_char(char):
    uart.write(char)

def receive_string():
    if uart.any():
        received_string = uart.readline()
        return received_string.decode('utf-8').rstrip('\n')
    return None

def send_string(string):
    uart.write(string + '\n')

def receive_number():
    if uart.any():
        received_data = uart.read(4)
        received_number = struct.unpack('I', received_data)[0]
        return received_number
    return None

def send_number(number):
    uart.write(struct.pack('I', number))

while True:
    # received_char = receive_char()
    # if received_char is not None:
    #     print("Received char:", received_char)
    #     send_char(received_char)

    received_string = receive_string()
    if received_string is not None:
        print("Received string:", received_string)
        send_string(received_string)

    received_number = receive_number()
    if received_number is not None:
        print("Received number:", received_number)
        send_number(received_number)

    utime.sleep_ms(10)

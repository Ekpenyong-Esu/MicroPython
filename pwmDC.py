from machine import Pin, PWM
import time

# Define the GPIO pin connected to the DC motor
motor_pin = 3

# Create a PWM object
pwm = PWM(Pin(motor_pin))

# Set the frequency of the PWM signal (start with 1000 Hz)
pwm.freq(1000)  # 1000 Hz

# Function to set the motor speed (duty cycle)
def set_speed(speed):
    # Map the speed (0 to 100) to the duty cycle (0 to 1023)
    duty_cycle = int(speed * 10.23)
    pwm.duty_u16(duty_cycle)

# Example: Vary the motor speed from minimum to maximum
for speed in range(0, 101, 5):
    set_speed(speed)
    time.sleep(0.5)  # Adjust the delay as needed for the desired speed change

# Stop the motor
set_speed(0)

# Turn off PWM
pwm.deinit()

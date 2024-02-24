from machine import Pin, PWM
import time

# Define the GPIO pin connected to the servo motor
servo_pin = 3

# Create a PWM object
pwm = PWM(Pin(servo_pin))

# Set the frequency of the PWM signal (usually 50 Hz for servo motors)
pwm.freq(50)  # 50 Hz

# Function to set the angle of the servo motor
def set_angle(angle):
    # Map the angle (in degrees) to the duty cycle (in microseconds)

    # (angle / 180) converts the angle to a ratio between 0 and 1.
    # Multiplying by 2000 scales this ratio to a range between 0 and 2000.
    # Adding 500 offsets the duty cycle to a range between 500 and 2500 microseconds.
    duty_cycle = int(500 + (angle / 180) * 2000)
    pwm.duty_ns(duty_cycle * 1000)  # Convert microseconds to nanoseconds

# Example: Sweep the servo motor from 0 to 180 degrees
for angle in range(0, 181, 10):
    set_angle(angle)
    time.sleep(0.5)  # Adjust the delay as needed for the desired speed

# Move the servo motor back to the starting position
set_angle(0)

# Turn off PWM
pwm.deinit()

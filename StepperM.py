from machine import Pin
import time

class StepperMotor:
    def __init__(self, pin1, pin2, pin3, pin4):
        self.coil_pins = [Pin(pin1, Pin.OUT),
                          Pin(pin2, Pin.OUT),
                          Pin(pin3, Pin.OUT),
                          Pin(pin4, Pin.OUT)]
        self.steps = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]
        self.step_delay = 0.01  # Adjust this for speed control

    def step(self, direction):
        for step in range(8):
            for coil in range(4):
                self.coil_pins[coil].value(self.steps[step][coil])
            time.sleep(self.step_delay)

# Define the pins connected to the stepper motor coils
# Replace these with the appropriate GPIO pin numbers
coil_pin1 = 0
coil_pin2 = 1
coil_pin3 = 2
coil_pin4 = 3

# Create an instance of the stepper motor
stepper_motor = StepperMotor(coil_pin1, coil_pin2, coil_pin3, coil_pin4)

# Example: Rotate the stepper motor 360 degrees clockwise

# Adjusting the 512 value in the code depends on the steps per revolution of your specific stepper motor. 
# You can calculate the appropriate number of steps based on the desired angle of rotation and the motor's 
# steps per revolution. For example, if your motor has 200 steps per revolution and you want to rotate it by 360 degrees, 
# you would need 200 * 360 / 360 = 200 steps.
for _ in range(512):
    stepper_motor.step(direction=1)  # 1 for clockwise, -1 for counterclockwise

# Pause for a moment
time.sleep(1)

# Example: Rotate the stepper motor 360 degrees counterclockwise
for _ in range(512):
    stepper_motor.step(direction=-1)  # 1 for clockwise, -1 for counterclockwise

# Cleanup GPIO pins
for pin in (coil_pin1, coil_pin2, coil_pin3, coil_pin4):
    Pin(pin, Pin.OUT).value(0)

import machine
import time

# Set the watchdog timer timeout in milliseconds
watchdog_timeout_ms = 5000  # 5 seconds

# Initialize the watchdog timer
watchdog = machine.WDT(timeout=watchdog_timeout_ms)

try:
    # Your main code here
    while True:
        print("Running main code...")
        time.sleep(1)

except Exception as e:
    print("Exception:", e)

finally:
    # This block will run when the script exits, whether it's normal or due to an exception
    print("Cleaning up and stopping watchdog.")
    watchdog.stop()

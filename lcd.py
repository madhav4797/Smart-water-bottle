import drivers
from time import sleep
from datetime import datetime

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

try:
    print("Writing to display")
    display.lcd_display_string("No time to waste", 1)  # Write line of text to $
    while True:
         display.lcd_display_string(str(datetime.now().time()), 2)
         
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program$
    print("Cleaning up!")
    display.lcd_clear()
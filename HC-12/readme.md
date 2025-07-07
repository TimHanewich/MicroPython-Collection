# HC-12

## Interfacing without Driver
Below is an example interfacing directly without the driver, if that is what you prefer:

```
from machine import Pin, UART
import time

# HC-12 connected to UART1 (GP4 = TX, GP5 = RX)
uart = UART(0, tx=Pin(16), rx=Pin(17), baudrate=9600)

# SET pin connected to GP3
set_pin = Pin(15, Pin.OUT)
set_pin.value(0)  # Enter AT command mode
time.sleep(0.1)   # Short delay to stabilize

# Send AT command
uart.write("AT+RX\r\n")  # Include carriage return and newline

# Wait for response
time.sleep(0.2)
if uart.any():
    response = uart.read()
    print("Response:", response)
else:
    print("No response received")
```
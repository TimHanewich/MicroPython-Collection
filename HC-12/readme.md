# HC-12

```
import machine
import time
from HC12 import HC12

# set up
uart = machine.UART(0, rx=machine.Pin(17), tx=machine.Pin(16)) # set up UART
set_pin = 15 # the pin you have the SET pin of the HC-12 connected to
hc12 = HC12(uart, set_pin)

# confirm it is working with a pulse
# sometimes this returns False when you first initialize it. Try again a few times and it'll usually work once the UART suffer is cleared.
print("HC-12 connected and operating: " + str(hc12.pulse))

# print the status: channel, transmission mode, transmitting power
print(hc12.status) # {'mode': 3, 'channel': 1, 'power': 8}

# receive
while True:
    print(hc12.receive()) # will return b'' if nothing received or data as bytes
    time.sleep(0.25)
```

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
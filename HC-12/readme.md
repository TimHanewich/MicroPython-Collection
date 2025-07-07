# HC-12
![HC-12](https://i.imgur.com/fPnVLDN.png)

The HC-12 is a versatile, low-power, long-range wireless serial communication module based on the Si4463 RF chip. Operating on the 433 MHz band, it supports transparent data transmission up to 1 kilometer (or more with optimal conditions and antenna setup). Its adjustable transmission power, flexible baud rate options, and simple UART interface make it ideal for hobbyist and professional projects alike—from remote sensor networks to robotics. Because it uses straightforward AT commands for configuration, it’s easy to integrate with a wide array of microcontrollers.

To streamline HC-12 integration with any MicroPython-capable microcontroller, I've developed a lightweight, user-friendly driver that handles communication and configuration tasks efficiently. Whether you're working with an ESP32, STM32, or the Raspberry Pi Pico (which I personally used during development), this driver simplifies setup and provides intuitive methods to send and receive data, modify parameters, and manage power states—all within MicroPython. It’s perfect for makers looking to add reliable wireless connectivity to their embedded projects without the overhead of writing serial routines from scratch.

The driver can be found here: [HC12.py](./HC12.py). Check out the sample code below for how to interface with it!

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

# or send
while True:
    ToSend:str = str(time.ticks_ms())
    hc12.send(ToSend.encode())
    time.sleep(5.0)
```

Note in the code above, the data sent and received from the HC-12 is of the `bytes` type. You can directly encode a `str` as `bytes` with `str.encode()` (i.e. `"Hello World".encode()`) and then decode `bytes` as a `str` with `bytes.decode()`.

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
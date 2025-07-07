import machine
import time
from HC12 import HC12

# set up
uart = machine.UART(0, rx=machine.Pin(17), tx=machine.Pin(16)) # set up UART
set_pin = 15 # the pin you have the SET pin of the HC-12 connected to
hc12 = HC12(uart, set_pin)

# confirm it is working with a pulse
print("HC-12 connected and operating: " + str(hc12.pulse))

# print the status: channel, transmission mode, transmitting power
print(hc12.status) # {'mode': 3, 'channel': 1, 'power': 8}

# Receive
while True:
    print(hc12.receive()) # will return b'' if nothing received or data as bytes
    time.sleep(0.25)
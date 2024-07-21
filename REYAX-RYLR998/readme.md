# REYAX RYLR998 Driver (Helper)
This is **in development**! It is a driver (helper) for interfacing with the [REYAX RYLR998 LoRa Module](https://reyax.com/products/RYLR998).

Here is [the RYLR998 datasheet that describes the AT commands required for interfacing with this module](https://github.com/TimHanewich/MicroPython-Collection/releases/download/2/LoRa_AT_Command_RYLR998_RYLR498_EN.pdf).

## Great learning resources
- https://mschoeffler.com/2020/12/19/lora-sender-receiver-communication-with-reyax-rylr896-breakout-boards-rylr890-modules/






## NOTES
Pico:
u = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))

Pico W:
u = machine.UART(0, baudrate=115200, tx=machine.Pin(12), rx=machine.Pin(13))
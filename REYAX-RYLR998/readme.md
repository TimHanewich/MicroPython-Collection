# REYAX RYLR998 Driver (Helper)
[reyax.py](./reyax.py) provides an easy-tou-use driver (helper) for interfacing with the [REYAX RYLR998 LoRa Module](https://reyax.com/products/RYLR998), allowing you to send data packets of information between two RYLR998 LoRa modules.

## Quick Start
To get up and running as quickly as possible with two new RYLR998 modules (default settings have not yet been modified), here is some sample code:

### Step 1: Set up Module A (on a separate device)
```
>>> import reyax
>>> import machine
>>> u = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))
>>> lora = reyax.RYLR998(u)
>>> lora.pulse # the pulse function returns True if a simple test command was able to validate the existence of the connected RYLR998 module.
True
>>> lora.networkid # each RYLR998 module belongs to a network ID, a group of devices that are to communicate with each other. 18 is default.
18
>>> lora.address # each RYLR998 module has a unique ID that it uses to send and receive as. 0 is default.
0
```

### Step 2: Set up Module B (on a separate device)
```
>>> import reyax
>>> import machine
>>> u = machine.UART(0, baudrate=115200, tx=machine.Pin(12), rx=machine.Pin(13))
>>> lora = reyax.RYLR998(u)
>>> lora.pulse
True
>>> lora.networkid
18
>>> lora.address = 1 # set the address of the second module, Module B, to 1.
>>> lora.address
1
```

### Step 3: Send Data!
With the first module, module A (address of `0`) set up as specified above, we're now able to send data from A to B!

```
>>> lora.send(1, "Hello, World!".encode("ascii"))
```

The line above sends the message "Hello, World!", encoded as ASCII bytes, to module with address `1` (module B).

To receive this message on module B, the module we set up above with address `1`, you can use the `receive()` function:

```
>>> msg = lora.receive()
>>> str(msg)
"{'address': 0, 'data': b'Hello, World!', 'RSSI': -27, 'SNR': 11, 'length': 13}"
```

The `receive()` function collects and parses any received message into a `ReceivedMessage` instance, with the following properties:
- `address` - The ID of the module the message was transmitted from.
- `length` - The length of the message (which can be inferred based on the data, of course).
- `data` - The data that was transmitted, in ASCII or otherwise.
- `RSSI` - Received signal strength indicator.
- `SNR` - Signal-to-noise ratio.

If multiple messages build up, they will be available to read in the order they came in. However, do not let this queue grow too big as the native Rx buffer on a microcontroller like a Pi Pico is rather small. You should frequently be reading to check for any available messages. 

If you try to read a message while there are none available, `None` will be returned:
```
>>> msg = lora.receive()
>>> str(msg)
'None'
```

Just like above, module B can *also* transmit data to module A at any time. No additional configuration needed.

### Sending Raw Data
Keep in mind that the data transmitted does not necessarily need to be in ASCII format.  You can transfer any raw sequence of bytes as well. For example, here we will transmit a 4-byte representation of a floating point number:

Sending from A:
```
>>> import struct
>>> lora.send(1, struct.pack("f", 3.14159)) # struct.pack converts the floating point number (3.14159) into 4 bytes.
```

Receiving on B:
```
>>> msg = lora.receive()
>>> str(msg)
"{'address': 0, 'data': b'\\xd0\\x0fI@', 'RSSI': -27, 'SNR': 11, 'length': 4}"
>>> import struct
>>> struct.unpack("f", msg.data)[0]
3.14159
```











## Official Documentation
- [REYAX RYLR998 Datasheet](https://github.com/TimHanewich/MicroPython-Collection/releases/download/3/RYLR998_EN.pdf)
- [REYAX RYLR998 AT Commands Specification](https://github.com/TimHanewich/MicroPython-Collection/releases/download/2/LoRa_AT_Command_RYLR998_RYLR498_EN.pdf)

## Great learning resources
- https://mschoeffler.com/2020/12/19/lora-sender-receiver-communication-with-reyax-rylr896-breakout-boards-rylr890-modules/






## NOTES
Pico:
u = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))

Pico W:
u = machine.UART(0, baudrate=115200, tx=machine.Pin(12), rx=machine.Pin(13))
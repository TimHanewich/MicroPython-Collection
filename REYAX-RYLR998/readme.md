# REYAX RYLR998 LoRa Module MicroPython Driver
![opening](https://i.imgur.com/r51HAFz.png)

The RYLR998 LoRa module by REYAX is a powerful and versatile wireless communication solution for IoT applications. With its long-range capabilities and low power consumption, it's an ideal choice for a wide range of projects, from smart sensors to industrial automation.

I've developed a MicroPython driver that allows developers to easily interface with the module from their microcontrollers. This driver provides a simple and intuitive API for sending and receiving data, configuring the module's settings, and monitoring its status.

[reyax.py](./reyax.py) provides an easy-to-use driver (helper) for interfacing with the [REYAX RYLR998 LoRa Module](https://reyax.com/products/RYLR998), allowing you to **easily** send data packets of information between two RYLR998 LoRa modules. I picked up two of these inexpensive modules [on Amazon](https://a.co/d/ebrZeHn)!

## Wiring
Wiring up and RYLR998 module to work with your microcontroller is very easy:
- **VDD** to a 3.3V supply on your microcontroller.
- **CND** to a ground pin on your microcontroller.
- **RXD** to a UART **TX** pin on your microcontroller.
- **TXD** to a UART **RX** pin on your microcontroller.

![wiring](https://i.imgur.com/ZI126QJ.jpeg)

## Code Quick Start
To get up and running as quickly as possible with two new RYLR998 modules (default settings have not yet been modified), here is some sample code:

### Step 1: Set up Module A
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

### Step 2: Set up Module B
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

## Advanced Configuration
The RYLR998 module has several settings that can be configured to cater to your particular use case. You'd typically modify these to further refine where you want your modules to perform on the tradeoff of speed and range.

### Center Frequency
We can use the `band()` function to change the center frequency that the RYLR998 module uses to transmit and receive messages. Lower frequencies can better penetrate walls and other objects, have longer range, and generally suffer from less interferance. However, higher frequencies benefit from faster data rates and lower latency.

The RYLR998 can operate between **820 MHz** and **960 MHz**. The transmitter and receiver must use the same frequency to communicate with each other, so make sure you set them both on the same frequency.

```
>>> lora.band
915000000
>>> lora.band = 820000000 # set to 820 MHz (820,000,000 Hz)
>>> lora.band
820000000
```

### RF Parameters
The RYLR998 module has several parameters that can be customized to further control how the module transmits and receives. We can access these four parameters using the `rf_parameters` property:

```
>>> lora.rf_parameters
(9, 7, 1, 12)
```

Each of the four integers above represents a unique RF parameter, described here in order:
- **Spreading Factor** - The Spreading Factor (SF) determines how much the LoRa signal is spread across the frequency band. It's a critical parameter that affects the trade-off between data rate, range, and interference robustness. A higher SF means the signal is spread more, resulting in longer range and better penetration through obstacles. A lower SF means the signal is spread less, resulting in a fast data rate, but shorter range and more susceptibility to interference.
- **Bandwidth** - The Bandwidth (BW) determines the frequency range used for LoRa transmission. A wider bandwidth allows for faster data rates, but also increases the susceptibility to interference. The RYLR998 supports three bandwidth settings: 125 KHz (default), 250 KHz, and 500 KHz. 125 KHz is narrowband, resistant to interferance while 500 KHz is wideband, faster, but more prone to interfernace, with the 250 KHz being a balance.
- **Coding Rate** - The Coding Rate (CR) determines the error correction capability of the LoRa transmission. It's a forward error correction (FEC) mechanism that adds redundancy to the data to detect and correct errors. A higher CR means more redundancy is added, resulting in better error correction capabilities but a slower data rate. A low CR means less redundance is added, resulting in a faster data rate, but is more prone to errors in transmission.
- **Programmed Preamble** - The Programmed Preamble (PP) is a sequence of bits transmitted at the beginning of each LoRa packet to help the receiver synchronize with the transmitter. A longer preamble (i.e. 16 symbols) provides better receiver synchronization and packet detection, but has longer transmission time. A shorter preamble (i.e. 8 symbols) provides faster transmission time but is a less robust.

To see what values each of these integer representations corresponds to, please see the `AT+PARAMETER` command description in the AT Commands sheet provided below.

To set these RF parameters, we can do so as a group as shown below:

```
lora.rf_parameters = (11, 9, 1, 12)
```

Sometimes you may get an error message like this:

```
>>> lora.rf_parameters = (8, 9, 1, 12)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "reyax.py", line 173, in rf_parameters
Exception: Setting parameters to (8, 9, 1, 12) failed with response b'+ERR=12\r\n+ERR=10\r\n'! A common mistake here is pairing together incompatible Spreading Factors and Bandwidths. Or, setting an incompatible programmed preamble for the module's current network ID. For more information, please see the AT+PARAMETER command specification in the AT COMMANDS documentation (see readme).
```

This often happens because you are trying to set a spreading factor and bandwidth to values that are incompatible with each other. The AT commands datasheet (access below) specifies that only certain spreading factors are available at certain bandwidths:
- At bandwidth 125 KHz:
    - Spreading Factor of 7
    - Spreading Factor of 8
    - Spreading Factor of 9
- At bandwidth 250 KHz:
    - Spreading Factor of 7
    - Spreading Factor of 8
    - Spreading Factor of 9
    - Spreading Factor of 10
- At bandwidth 500 KHz:
    - Spreading Factor of 7
    - Spreading Factor of 8
    - Spreading Factor of 9
    - Spreading Factor of 10
    - Spreading Factor of 11

**REMEMBER: For your modules to communicate with each other, all RF parameters must be set to the same values on both modules!**

### RF Output Power
The RF output power, a measure of the power of the radio frequency signal transmitted expressed in decibels relative to one milliwatt (dbM), can be modified.

The power can be set to between 0 and 22 dBm, with 22 dBm (the most powerful broadcast) being the default. To read/change the output power:

```
>>> lora.output_power
22
>>> lora.output_power = 10
>>> lora.output_power
10
```

### Change UART Baud Rate
The RYLR998 module can interface with your microcontroller over UART using several different baud rates (transmission speeds from your microcontroller to the module over the wire, not to be confused with the radio transmission speed between modules). While I don't recommend changing the baud rate (the default of 115200 has proved to work well), it can be adjusted:

```
>>> lora.baudrate
115200
>>> lora.baudrate = 9600
>>> lora.baudrate
9600
```

Since this only defines the baud rate speed between the module and the microcontroller you are using to control it, the baud rates used by both modules do not need to match; this has nothing to do with RF transmission/receiving.

## Other Data
The RYLR998 also provides a few other commands that can be used to access data about the module you are using.

### Module ID
Use the `UID` property (short for "unique ID") to access the model ID, a unique ID assigned to that particular RYLR998 module:

```
>>> lora.UID
'0014003104691F6900001B06'
```

### Firmware Version
Use the `version` property to access the firmware version that is running on your RYLR998 module:

```
>>> lora.version
'RYLR998_REYAX_V1.2.3'
```


## Official Documentation
- [REYAX RYLR998 Datasheet](https://github.com/TimHanewich/MicroPython-Collection/releases/download/3/RYLR998_EN.pdf)
- [REYAX RYLR998 AT Commands Specification](https://github.com/TimHanewich/MicroPython-Collection/releases/download/2/LoRa_AT_Command_RYLR998_RYLR498_EN.pdf)
- [REYAX RYLR998 STL File (3D model)](https://github.com/TimHanewich/MicroPython-Collection/releases/download/4/RYLR998.stl)

## Great learning resources
- https://mschoeffler.com/2020/12/19/lora-sender-receiver-communication-with-reyax-rylr896-breakout-boards-rylr890-modules/






## NOTES
Pico:
u = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))

Pico W:
u = machine.UART(0, baudrate=115200, tx=machine.Pin(12), rx=machine.Pin(13))
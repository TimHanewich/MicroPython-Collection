# USB Communications
The Raspberry Pi Pico, through MicroPython, allow you to maintain constant a bidirecitonal stream of serial communication with a PC it is plugged into.

## Pico Example
[This example](./example-pico/main.py) offers a simple demonstration of using MicroPython to communicate with the client PC over the USB serial line bidirectionaly.

This example is *slightly more complicated* than most simple examples you can find online, but I favor this method as it is:
- Non-blocking: it allows for the collection of bytes, one by one, and then will proceed with processing, coming back to read later on, allowing a workflow to continue until all the data has been received and is ready to be processed
- **Binary**: it allows for the streaming information to be in binary form.





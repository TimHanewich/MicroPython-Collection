"""
Lightweight driver for interfacing with the RYLR998 LoRa module by REYAX.
Author Tim Hanewich, github.com/TimHanewich
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/blob/master/REYAX-RYLR998/

MIT License
Copyright 2024 Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import machine

class RYLR998:

    def __init__(self, uart:machine.UART) -> None:
        self._uart = uart
        
        # clear RX buffer to start
        self._clearrx()

    def send(self, address:int, data:bytes) -> None:
        """Send a packet of binary data to a specified address."""

        # max length that can be sent in one go is 240
        if len(data) > 240:
            raise Exception("Provided data packet of length " + str(len(data)) + " to send is too large! Limit is 240 bytes.")

        # form base command and encode to bytes
        cmd:str = "AT+SEND=" + str(address) + "," + str(len(data)) + ","
        cmd_ba:bytearray = bytearray(cmd.encode())

        # append data to send
        cmd_ba.extend(data)
        
        # append \r\n (newline)
        cmd_ba.extend("\r\n".encode())
        
        # send!
        self._uart.write(cmd_ba)

        print("Just sent: " + str(bytes(cmd_ba)))

    def _clearrx(self) -> None:
        """Clears all bytes from the Rx buffer by reading all."""
        while True:
            if (len(self._readall())) == 0:
                break

    def _readline(self) -> bytes:
        """Read a line, ending in newline character (\n)"""
        return self._uart.readline()
    
    def _any(self) -> int:
        """Returns the number of bytes available on the Rx line available for reading."""
        return self._uart.any()

    def _readall(self) -> bytes:
        """Returns all bytes available for reading on the Rx line (held in buffer)."""
        return self._uart.read(self._uart.any())
        
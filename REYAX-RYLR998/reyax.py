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
import time

class ReceivedMessage:
    def __init__(self) -> None:
        self.address:int = None # the address of the transmitter it came from
        self.length:int = None # the length (number of bytes) of the data payload
        self.data:bytes = None # the payload data itself
        self.RSSI:int = None # Received signal strength indicator
        self.SNR:int = None # Signal-to-noise ratio

    def parse(self, full_line:bytes) -> None:
        """Parses a received message from the raw line of byte data received over UART. For example, b'+RCV=50,5,HELLO,-99,40'"""

        # find landmarkers that will help with parsing
        i_equal:int = full_line.find("=".encode("ascii"))
        i_comma1:int = full_line.find(",".encode("ascii"))
        i_comma2:int = full_line.find(",".encode("ascii"), i_comma1 + 1)
        i_comma4:int = full_line.rfind(",".encode("ascii")) # search from end
        i_comma3:int = full_line.rfind(",".encode("ascii"), 0, i_comma4-1) # search for a comma from right, starting at 0 and ending at the last comma (or right before it)
        i_linebreak:int = full_line.find("\r\n".encode("ascii"))
        
        # extract
        self.ReceivedMessage = ReceivedMessage()
        self.address = int(full_line[i_equal + 1:i_comma1].decode("ascii"))
        self.length = int(full_line[i_comma1 + 1:i_comma2].decode("ascii"))
        self.data = full_line[i_comma2 + 1:i_comma3]
        self.RSSI = int(full_line[i_comma3 + 1:i_comma4].decode("ascii"))
        self.SNR = int(full_line[i_comma4 + 1:i_linebreak].decode("ascii"))

    def __str__(self) -> str:
        return str({"address":self.address, "length":self.length, "data":self.data, "RSSI":self.RSSI, "SNR":self.SNR})

class RYLR998:

    def __init__(self, uart:machine.UART) -> None:
        self._uart = uart

        # clear out UART Rx buf
        while self._uart.any() > 0:
            self._uart.read()

        # set up internal RX buffer
        self._rxbuf:bytes = bytes()

    @property
    def pulse(self) -> bool:
        """Runs a simple test command to the RYLR998 module to validate it is connected and functioning properly."""
        response:bytes = self._command_response("AT\r\n".encode("ascii"))
        return response == "+OK\r\n".encode("ascii")

    @property
    def UID(self) -> str:
        """Unique identifier of this particular RYLR998 module."""
        return self._command_response("AT+UID?\r\n".encode("ascii"))[5:-2].decode("ascii")
    
    @property
    def version(self) -> str:
        """The firmware version of this particular RYLR998 module."""
        return self._command_response("AT+VER?\r\n".encode("ascii"))[5:-2].decode("ascii")

    @property
    def networkid(self) -> int:
        """The network ID is the group of RYLR998 modules that are tuned in to each other."""
        response:bytes = self._command_response("AT+NETWORKID?\r\n".encode("ascii"))
        i_equal = response.find("=".encode("ascii"))
        if i_equal == -1:
            raise Exception("Network ID read request did not return a valid network ID! (no = sign in response)")
        return int(response[i_equal+1:].decode("ascii"))
    
    @networkid.setter
    def networkid(self, value:int) -> None:
        valid_ids:list[int] = [3,4,5,6,7,8,9,10,11,12,13,14,15,18]
        if value not in valid_ids: # valid network ID's according to datasheet
            raise Exception("Network ID of '" + str(value) + "' is invalid. Must be a valid network ID: " + str(valid_ids))
        response:bytes = self._command_response("AT+NETWORKID=".encode("ascii") + str(value).encode("ascii") + "\r\n".encode("ascii"))
        if response != "+OK\r\n".encode("ascii"):
            raise Exception("Setting network ID to '" + str(value) + "' failed with response '" + str(response) + "'")
        
    @property
    def address(self) -> int:
        """The address the RYLR998 will use to self-identify with when transmitting and receiving."""
        response:bytes = self._command_response("AT+ADDRESS?\r\n".encode("ascii"))
        i_equal = response.find("=".encode("ascii"))
        if i_equal == -1:
            raise Exception("Address read request did not return a valid network ID! (no = sign in response)")
        return int(response[i_equal+1:].decode("ascii"))
    
    @address.setter
    def address(self, value:int) -> None:
        if value < 0 or value > 65535: # valid addresses according to datasheet
            raise Exception("Address of '" + str(value) + "' is invalid. Must be between 0-65535.")
        response:bytes = self._command_response("AT+ADDRESS=".encode("ascii") + str(value).encode("ascii") + "\r\n".encode("ascii"))
        if response != "+OK\r\n".encode("ascii"):
            raise Exception("Setting address to '" + str(value) + "' failed with response '" + str(response) + "'")
        
    @property
    def baudrate(self) -> int:
        """The UART baud rate the RYLY988 is using to communicate."""
        response:bytes = self._command_response("AT+IPR?\r\n".encode("ascii"))
        i_equal = response.find("=".encode("ascii"))
        if i_equal == -1:
            raise Exception("Baud rate read request did not return a valid rate! (no = sign in response)")
        return int(response[i_equal+1:].decode("ascii"))
    
    @baudrate.setter
    def baudrate(self, value:int) -> None:
        acceptable_rates:list[int] = [300,1200,4800,9600,19200,28800,38400,57600,115200]
        if value not in acceptable_rates:
            raise Exception("You cannot set a baud rate of '" + str(value) + "'! Baud rate must be one of these: " + str(acceptable_rates))
        response:bytes = self._command_response("AT+IPR=".encode("ascii") + str(value).encode("ascii") + "\r\n".encode("ascii"))
        if response.find("+IPR=".encode("ascii") + str(value).encode("ascii") + "\r\n".encode("ascii")) == -1:
            raise Exception("Setting baud rate to '" + str(value) + "' failed! Confirmation message not heard back.")
        else: # We found the confirmation, it was successful! 
            self._uart.init(value) # adjust to the new baudrate so any subsequent communication is read + sent correctly.

        



    def software_reset(self) -> None:
        """Software reset of RYLR998 module."""
        response:bytes = self._command_response("AT+RESET\r\n")
        if response != "+RESET\r\n+READY\r\n".encode("ascii"):
            raise Exception("Software reset was not confirmed to be successful! Response '" + str(response) + "' received instead of standard +RESET and +READY!")


    def send(self, address:int, data:bytes) -> None:
        """Send a packet of binary data to a specified address."""

        # max length that can be sent in one go is 240
        if len(data) > 240:
            raise Exception("Provided data packet of length " + str(len(data)) + " to send is too large! Limit is 240 bytes.")

        # assemble the command
        cmd:bytes = bytes()
        cmd += "AT+SEND=".encode("ascii")
        cmd += str(address).encode("ascii") + ",".encode("ascii")
        cmd += str(len(data)).encode("ascii") + ",".encode("ascii")
        cmd += data
        cmd += "\r\n".encode("ascii")

        # send the command, get the response
        response:bytes = self._command_response(cmd, 1.0)

        # if not successful
        if response != "+OK\r\n".encode("ascii"):
            raise Exception("Send command '" + str(cmd) + "' returned abnormal response '" + str(response) + "'")
        
    def receive(self) -> ReceivedMessage:
        """If there is a message awaiting retrieval, returns it."""

        # collect anything on the Rx to local buffer
        self._colrx()

        # find where the +RCV (receive message start) starts
        i1:int = self._rxbuf.find("+RCV=".encode("ascii")) # find where the received message starts

        # if there is no message to be found, return None
        if i1 == -1: 
            return None
    
        # find where it ends from here (newline)
        i2:int = self._rxbuf.find("\r\n".encode("ascii"), i1 + 1)

        # if no \r\n found
        if i2 == -1:
            raise Exception("Received message beginning at index '" + str(i1) + "' in internal buf did not terminate in '\\r\\n'")
        
        # get bytes of the full RCV
        rcv:bytes = self._rxbuf[i1:i2 + 2] # add +2 for  the length of the \r\n (actually 2 characters)

        # "pluck" it out
        self._rxbuf = self._rxbuf[0:i1] + self._rxbuf[i2+2:]

        # now time to convert the RCV message to useful data
        ToReturn:ReceivedMessage = ReceivedMessage()
        ToReturn.parse(rcv)

        return ToReturn
        


    def _colrx(self) -> None:
        """Collects and moves all bytes from UART Rx buffer to internal buffer."""
        all_bytes:bytes = self._uart.read()
        if all_bytes != None:
            self._rxbuf += all_bytes
    
    def _command_response(self, command:bytes, response_delay:float = 0.5)-> bytes:
        """Sends a byte sequence (AT command) to the RYLR988 module, and collects the response while still preserving any pre-existing bytes in the internal Rx buffer."""

        # collect any bytes still left over in UART Rx and make note of the length of the internal buffer before the command is sent out and response for it is received
        self._colrx()
        len_before:int = len(self._rxbuf)

        # send command
        self._uart.write(command)

        # wait a little for it to be processed and then the response to arrive
        time.sleep(response_delay)

        # collect any new bytes in UART Rx
        self._colrx()

        # count the number of new bytes that were just added!
        new_bytes_count:int = len(self._rxbuf) - len_before

        # if there are not any new bytes in the internal buf, it failed!
        if new_bytes_count == 0:
            raise Exception("Response from RYLY998 for command " + str(command) + " was not received after waiting " + str(response_delay) + " seconds!")
        
        # get the ones we just received
        response:bytes = self._rxbuf[-new_bytes_count:]

        # trim the internal buffer now that we just "plucked" the response out of it
        self._rxbuf = self._rxbuf[0:-new_bytes_count]

        return response


u = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))
r = RYLR998(u)
print(r.pulse)
print(r._rxbuf)

r.baudrate = 115200
print(r._rxbuf)
print(r.pulse)
print(r.baudrate)

r.baudrate = 9600
print(r._rxbuf)
print(r.pulse)
print(r.baudrate)

r.baudrate = 115200
print(r._rxbuf)
print(r.pulse)
print(r.baudrate)
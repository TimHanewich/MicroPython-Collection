import machine
import time

class HC12:

    def __init__(self, uart:machine.UART, SET_pin:int):

        # primary I/O (UART and the SET pin)
        self._uart = uart
        self._set_pin = machine.Pin(SET_pin, machine.Pin.OUT)

        # Internal process variables
        self._rx_buffer:bytearray = bytearray()
        self._procTime:float = 0.15 # standard processing time used across functions

        # set up
        self._uart.init(baudrate=9600, timeout=200, timeout_char=10) # re-init with required param values
        self._uart.read() # clear RX buffer

    def _flush_rx(self) -> int:
        """Read all bytes on the UART RX buffer and bring them into an internal buffer. Returns the number of new bytes that were read and captured."""
        if self._uart.any() > 0: # if there is data to receive
            new_data:bytes = self._uart.read()
            self._rx_buffer = self._rx_buffer + new_data
            return len(new_data)
        else:
            return 0

    def receive(self) -> bytes:
        """Returns any bytes that have been received (intentionally excludes any AT command responses)."""
        self._flush_rx() # read anything else awaiting on the UART RX buffer
        ToReturn:bytes = bytes(self._rx_buffer) # prepare to return
        self._rx_buffer = bytearray() # clear the internal RX buffer
        return ToReturn
    
    def send(self, data:bytes) -> None:
        """Sends data via the HC-12."""
        self._set_pin.high() # put set pin in high, its normal state for sending data (not sending AT commands)... it should be in this anyway, but doing it again to be sure.
        self._uart.write(data)
    
    @property
    def pulse(self) -> bool:
        response = self._command_response("AT\r\n".encode())
        return response == "OK\r\n".encode()
            
    @property
    def channel(self) -> int:
        """Checks which channel the HC-12 is currently operating on."""
        response:bytes = self._command_response("AT+RC\r\n".encode())
        responseSTR:str = response.decode()
        if responseSTR.startswith("OK+RC"):
            return int(responseSTR[5:])
        else:
            raise Exception("Unable to extract channel value from HC-12 response '" + str(response) + "'.")
        
    @property
    def power(self) -> int:
        """Checks the transmitter power, in dBm, the HC-12 is currently using."""
        response:bytes = self._command_response("AT+RP\r\n".encode())
        responseSTR:str = response.decode()  # 'b'OK+RP:-01dBm\r\n'', 'b'OK+RP:+20dBm\r\n''
        if responseSTR.startswith("OK+RP:"):
            return int(responseSTR[7:9])
        else:
            raise Exception("Unable to extract transmitting power value from HC-12 response '" + str(response) + "'.")
        
    @power.setter
    def power(self, level:int) -> None:
        """Set the transmitting power to a level between 1-8."""
        asstr:str = "AT+P" + str(level) + "\r\n"
        response:bytes = self._command_response(asstr.encode())
        if "OK+P".encode() not in response:
            raise Exception("Unable to set transmitting power to " + str(level) + "!")
        
    @property
    def mode(self) -> int:
        """Returns the transmission mode of the HC-12, either 1, 2, 3, or 4"""

        # We have to handle this one differently than using the ._command_response() function because this one gives a whole bunch of lines and takes a moment.
        # there is no way to get ONLY the transmission mode (FU) with a commmand. We have to ask for all the parameters and parse it out

        # enter into AT mode
        self._set_pin.low() # pull it low to go into AT mode
        time.sleep(self._procTime) # wait a moment for AT mode to be realized

        # flush the existing buffer so what we get next is for sure the response from the AT command
        self._flush_rx()

        # write AT command
        self._uart.write("AT+RX\r\n".encode())

        # get full response
        # the last part of the transmission should be the OK+FU, what we are looking for
        started_at_ticks_ms:int = time.ticks_ms()
        response:bytes = bytes()
        while "OK+FU".encode() not in response or (time.ticks_ms() - started_at_ticks_ms) > 1000:
            time.sleep(self._procTime)
            data:bytes = self._uart.readline()
            if data != None:
                response = response + data

        # enter back into normal mode
        self._set_pin.high()

        # parse out transmission mode (FU)
        if response.endswith("OK+FU1\r\n".encode()):
            return 1
        elif response.endswith("OK+FU2\r\n".encode()):
            return 2
        elif response.endswith("OK+FU3\r\n".encode()):
            return 3
        elif response.endswith("OK+FU4\r\n".encode()):
            return 4
        else:
            raise Exception("Unable to interpret transmission mode from response '" + str(response) + "'")
    
    @mode.setter
    def mode(self, mode:int) -> None:
        """Set the transmission mode of the HC-12 as FU1, FU2, FU3, or FU4."""
        if mode not in [1,2,3,4]:
            raise Exception("Transmission mode must be either 1, 2, 3, or 4.")
        cmd:str = "AT+FU" + str(mode) + "\r\n"
        response:bytes = self._command_response(cmd.encode())
        if "OK+FU".encode() not in response:
            raise Exception("Setting transmission mode to " + str(mode) + " was not successful. Response from HC-12 was '" + str(response) + "'")

    def _command_response(self, cmd:bytes) -> bytes:
        """Brokers the sending of AT commands and collecting a response. Returns None if nothing was received."""

        # enter into AT mode
        self._set_pin.low() # pull it low to go into AT mode
        time.sleep(self._procTime) # wait a moment for AT mode to be realized

        # flush the existing buffer so what we get next is for sure the response from the AT command
        self._flush_rx()

        # write AT
        self._uart.write(cmd)

        # wait for response
        response:bytes = self._uart.readline()

        # enter back into normal mode
        self._set_pin.high()

        return response


import machine
import time

uart = machine.UART(0, rx=machine.Pin(17), tx=machine.Pin(16))
hc12 = HC12(uart, 15)

print(hc12.pulse)
print(hc12.channel)
print(hc12.power)
print(hc12.mode)
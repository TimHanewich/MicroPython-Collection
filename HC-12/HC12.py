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
        self._uart.read() # clear RX buffer

    def _flush_rx(self) -> int:
        """Read all bytes on the UART RX buffer and bring them into an internal buffer. Returns the number of new bytes that were read and captured."""
        if self._uart.any() > 0: # if there is data to receive
            new_data:bytes = self._uart.read()
            self._rx_buffer = self._rx_buffer + new_data
            return len(new_data)
        else:
            return 0

    def read(self) -> bytes:
        """Returns any bytes that have been received (intentionally excludes any AT command responses)."""
        self._flush_rx() # read anything else awaiting on the UART RX buffer
        ToReturn:bytes = bytes(self._rx_buffer) # prepare to return
        self._rx_buffer = bytearray() # clear the internal RX buffer
        return ToReturn
    
    def send(self, data:bytes) -> None:
        """Sends data via the HC-12."""
        self._uart.write(data)

    @property
    def pulse(self) -> bool:
        """Runs a simple test to validate the HC-12 is connected and operating."""
        try:
            response:bytes = self._command_response("AT\r\n".encode(), "OK\r\n".encode())
            return response == "OK\r\n".encode()
        except: # error was raised, i.e. it did not response at all! (not even plugged in and working?)
            return False
    
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
        expected:str = "OK+P" + str(level) + "\r\n"
        response:bytes = self._command_response(asstr.encode(), expected.encode())
        if "OK+P".encode() not in response:
            raise Exception("Unable to set transmitting power to " + str(level) + "!")
        
    @property
    def mode(self) -> int:
        """Returns the transmission mode of the HC-12, either 1, 2, 3, or 4"""
        response:bytes = self._command_response("AT+RX\r\n".encode(), expected=None, timeout_ms=1000) # Example: b'OK+B9600\r\nOK+RC001\r\nOK+RP:+08dBm\r\nOK+FU3\r\n'. I find the second half of that takes a bit of time to populate, so adding extra long timeout
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
        expected:str = "OK+FU" + str(mode) + "\r\n"
        response:bytes = self._command_response(cmd.encode(), expected.encode())
        if response != expected.encode():
            raise Exception("Setting transmission mode to " + str(mode) + " was not successful. Response from HC-12 was '" + str(response) + "'")

    def _command_response(self, cmd:bytes, expected:bytes = None, timeout_ms:int = 500) -> bytes:
        """
        Brokers the sending of AT commands and collecting a response.
        If you do NOT provide a expected value, it will wait the entirety of the timeout to collect all bytes in that period.
        If you DO provide an expected value, it will stop waiting as soon as it receives what you expected, not waiting the entire timeout (faster).
        """

        # enter into AT mode
        self._set_pin.low() # pull it low to go into AT mode
        time.sleep(self._procTime) # wait a moment

        # send data
        self._flush_rx()
        len_before:int = len(self._rx_buffer) # record the length of the RX buffer BEFORE we send (for comparison purposes later)
        self._uart.write(cmd) # write the command

        # receive!
        if expected == None: # if they did not specify what they are expecting, just wait the full timeout
            time.sleep_ms(timeout_ms)
            self._flush_rx()
        else: # if they did specify, then wait until we receive it and then terminate
            started_at_ticks_ms = time.ticks_ms()
            while (time.ticks_ms() - started_at_ticks_ms) < timeout_ms:
                nb:int = self._flush_rx() # "br" short for bytes received, the number of new bytes received
                if nb > 0:
                    if self._rx_buffer.endswith(expected):
                        break
                time.sleep_ms(1)
        len_after:int = len(self._rx_buffer)

        # We either received data just now or just hit the timeout
        # If we received nothing new, that means we hit a timeout. So raise an exception because we didn't get an expected response.
        if len_after == len_before:
            raise Exception("No response from HC-12 module after waiting " + str(timeout_ms) + " ms for response from command '" + str(cmd) + "'.")
        
        # piece out what we just received
        response:bytes = bytes(self._rx_buffer[-len_after:]) # get the last X bytes we just received
        self._rx_buffer[-len_after:] = b'' # delete the last X bytes we just received

        # go back into non-AT mode (normal mode)
        self._set_pin.high() # pull it high to return to normal mode
        time.sleep(self._procTime) # wait a moment

        return response
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

    def _flush_rx(self) -> int:
        """Read all bytes on the UART RX buffer and bring them into an internal buffer. Returns the number of new bytes that were read and captured."""
        if self._uart.any() > 0: # if there is data to receive
            new_data:bytes = self._uart.read()
            self._rx_buffer = self._rx_buffer + new_data
            return len(new_data)
        else:
            return 0

    @property
    def pulse(self) -> bool:
        """Runs a simple test to validate the HC-12 is connected and operating."""
        try:
            return self._command_response("AT\r\n".encode()) == "OK\r\n".encode()
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
        response:bytes = self._command_response(asstr.encode())
        if "OK+P".encode() not in response:
            raise Exception("Unable to set transmitting power to " + str(level) + "!")

    def _command_response(self, cmd:bytes, timeout_ms:int = 500) -> bytes:
        """Brokers the sending of AT commands and collecting a response."""

        # enter into AT mode
        self._set_pin.low() # pull it low to go into AT mode
        time.sleep(self._procTime) # wait a moment

        # send data
        self._flush_rx()
        len_before:int = len(self._rx_buffer) # record the length of the RX buffer BEFORE we send (for comparison purposes later)
        self._uart.write(cmd) # write the command
        
        # Wait for data to be received or until we hit the timeout
        ReceivedAtLeastOneByte:bool = False # tracker that we have received at least one new byte
        started_at_ticks_ms = time.ticks_ms()
        while (time.ticks_ms() - started_at_ticks_ms) < timeout_ms:
            br:int = self._flush_rx() # "br" short for bytes received, the number of new bytes received
            if br >= 1: # if we received at least one new byte
                ReceivedAtLeastOneByte = True # flag as true
            else: # if we did NOT receive at least one new byte
                if ReceivedAtLeastOneByte: # But if we received one earlier, that means we must be at the END of the transmission
                    break # so break out of this loop... the receiving is done!
            time.sleep_ms(50) # wait a moment
        len_after:int = len(self._rx_buffer)

        # We either received data just now or just hit the timeout
        # If we received nothing new, that means we hit a timeout. So raise an exception because we didn't get an expected response.
        if len_after == len_before:
            raise Exception("No response from HC-12 module after waiting " + str(timeout_ms) + " ms for command '" + str(cmd) + "'.")
        
        # piece out what we just received
        response:bytes = self._rx_buffer[-len_after:] # get the last X bytes we just received
        self._rx_buffer[-len_after:] = b'' # delete the last X bytes we just received

        # go back into non-AT mode (normal mode)
        self._set_pin.high() # pull it high to return to normal mode
        time.sleep(self._procTime) # wait a moment

        return response

    
uart = machine.UART(0, tx=machine.Pin(16), rx=machine.Pin(17))

hc12 = HC12(uart, 15)
print(hc12.pulse)
print(hc12.channel)
hc12.power = 4
print(hc12.power)
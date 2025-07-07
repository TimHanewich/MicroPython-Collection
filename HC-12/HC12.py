import machine
import time

class HC12:

    def __init__(self, uart:machine.UART, SET_pin:int):
        self._uart = uart
        self._set_pin = machine.Pin(SET_pin, machine.Pin.OUT)
        self._procTime:float = 0.15 # processing time

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
        if response.startswith("OK+P".encode()) == False:
            raise Exception("Unable to set transmitting power to " + str(level) + "!")

    def _command_response(self, cmd:bytes, timeout_ms:int = 500) -> bytes:
        """Brokers the sending of AT commands and collecting a response."""

        # enter into AT mode
        self._set_pin.low() # pull it low to go into AT mode
        time.sleep(self._procTime) # wait a moment
        
        # send data
        self._uart.read() # clears the RX buffer first 
        self._uart.write(cmd) # write the command
        
        # Wait for data to be received or until we hit the timeout
        started_at_ticks_ms = time.ticks_ms()
        while (time.ticks_ms() - started_at_ticks_ms) < timeout_ms:
            if self._uart.any() > 0: # if we have bytes on the line, break out of the while loop
                break
            else: # no bytes yet, wait a bit
                time.sleep(self._procTime)

        # If there is not data to be received (we must have hit our timeout), raise Exception
        if self._uart.any() == 0:
            raise Exception("No response from HC-12 module after waiting " + str(timeout_ms) + " ms for command '" + str(cmd) + "'.")
        else: # there is at least 1 byte!
            time.sleep(self._procTime) # give it an extra moment for any more bytes to finish being received
        
        # receive it
        response:bytes = self._uart.read()

        # go back into non-AT mode (normal mode)
        self._set_pin.high() # pull it high to return to normal mode
        time.sleep(self._procTime) # wait a moment

        return response

    
uart = machine.UART(0, tx=machine.Pin(16), rx=machine.Pin(17))

hc12 = HC12(uart, 15)
print(hc12.pulse)
print(hc12.channel)
hc12.power = 5
print(hc12.power)
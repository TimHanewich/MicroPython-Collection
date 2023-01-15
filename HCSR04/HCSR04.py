# Version: 1
# Written by Tim Hanewich

import machine
import utime
import time

class HCSR04:

    trigger = None
    echo = None

    def __init__(self, trigger:int, echo:int) -> None:
        self.trigger = machine.Pin(trigger, machine.Pin.OUT)
        self.echo = machine.Pin(echo, machine.Pin.IN)

    # returns distance in centimeters
    def measure(self) -> float:
        self.trigger.low()
        utime.sleep_us(2)

        self.trigger.high()
        utime.sleep_us(5)
        self.trigger.low()

        while self.echo.value() == 0:
            signaloff = utime.ticks_us()
        
        while self.echo.value() == 1:
            signalon = utime.ticks_us()
        
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        return distance
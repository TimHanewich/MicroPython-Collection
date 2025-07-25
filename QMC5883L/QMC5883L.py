"""
QMC5883L.py - lightweight MicroPython driver for interfacing with the QMC5883L magnetometer (compass).
For any updates and instructions on how to use this, visit: https://github.com/TimHanewich/MicroPython-Collection/tree/master/QMC5883L
Author Tim Hanewich, github.com/TimHanewich

MIT License
Copyright 2025 Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import machine
import math

class QMC5883L:

    def __init__(self, i2c:machine.I2C):
        self._i2c = i2c
        self._address = 0x0D
        self.initialize()

    def initialize(self) -> None:
        """Initializes the QMC5883L."""
        self._i2c.writeto_mem(self._address, 0x09, bytes([0x1D])) # 0x1D = 0b00011101: 10Hz output, continuous mode, oversampling x64, full scale
        self._i2c.writeto_mem(self._address, 0x0A, bytes([0x00])) # no interrupts

    def read(self) -> tuple[int, int, int]:
        """Read the magnetometer values in X,Y,Z format."""
        raw_data:bytes = self._i2c.readfrom_mem(self._address, 0x00, 6) # read 6 bytes
        x:int = int.from_bytes(raw_data[0:2], "little")
        y:int = int.from_bytes(raw_data[2:4], "little")
        z:int = int.from_bytes(raw_data[4:6], "little")
        return (x, y, z)
    
    def calibrate(self, x_min:int, x_max:int, y_min:int, y_max:int, z_min:int, z_max:int) -> None:
        """Stores the extrema of the observed raw XYZ readings, which will later be used in determining compass heading."""
        self._x_min:int = x_min
        self._x_max:int = x_max
        self._y_min:int = y_min
        self._y_max:int = y_max
        self._z_min:int = z_min
        self._z_max:int = z_max

    @property
    def heading(self) -> float:
        """Determines the magnetometer's current heading using the X and Y values (assuming it is laying flat)."""
        x,y,z = self.read()
        x_cal:float = x - (self._x_min + self._x_max) / 2 # subtract the average (midpoint) X value out, so the reading is "centered" at 0
        y_cal:float = y - (self._y_min + self._y_max) / 2 # subtract the average (midpoint) Y value out, so the reading is "centered" at 0
        heading_rad = math.atan2(y_cal, x_cal) # heading, in radians
        heading_deg = math.degrees(heading_rad) # heading, in degrees
        if heading_deg < 0:
            heading_deg += 360
        return heading_deg
"""
ENS160.py MicroPython driver for the ENS160 Digital Metal-Oxide Multi-Gas Sensor manufactured by ScioSense - https://www.sciosense.com/products/environmental-sensors/ens160-digital-multi-gas-sensor/
Author Tim Hanewich, github.com/TimHanewich
Version 1.2, August 21, 2023
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/blob/master/ENS160/ENS160.py

MIT License
Copyright 2023 Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import machine
import time

class ENS160:
    """
    Lightweight class for communicating with an ENS160 air quality sensor via I2C.
    Follows the specifications defined in the official ENS160 data sheet: https://www.mouser.com/datasheet/2/1081/SC_001224_DS_1_ENS160_Datasheet_Rev_0_95-2258311.pdf
    Newer version of ENS160 data sheet: https://www.sciosense.com/wp-content/uploads/documents/SC-001224-DS-9-ENS160-Datasheet.pdf
    """
    
    def __init__(self, i2c:machine.I2C, address:int = 0x53):
        """
        Creates a new instance of the ENS160 class
        :param i2c: Setup machine.I2C interface
        :param address: The I2C address of the ENS160 slave device
        """
        self.address = address
        self.i2c = i2c
    
    @property
    def operating_mode(self) -> int:
        """
        Reads the operating mode that the ENS160 is currently in.
        0 = Deep Sleep Mode (low power standby)
        1 = Idle mode (low-power)
        2 = Standard Gas Sensing Mode
        """
        return self.i2c.readfrom_mem(self.address, 0x10, 1)[0]
    
    @operating_mode.setter
    def operating_mode(self, value):
        """
        Sets the ENS160's operating mode.
        0 = Deep Sleep Mode (low power standby)
        1 = Idle mode (low-power)
        2 = Standard Gas Sensing Mode
        """
        if value not in [0, 1, 2, 0xF0]:
            raise Exception("Operating value you're setting must be 0, 1, or 2")
        self.i2c.writeto_mem(self.address, 0x10, bytes([value]))
        
    @property
    def CO2(self) -> int:
        """Reads the calculated equivalent CO2-concentration in PPM, based on the detected VOCs and hydrogen"""
        bs = self.i2c.readfrom_mem(self.address, 0x24, 2)
        return self._translate_pair(bs[1], bs[0])
        
    @property
    def TVOC(self) -> int:
        """Reads the calculated Total Volatile Organic Compounds (TVOC) concentration in ppb"""
        bs = self.i2c.readfrom_mem(self.address, 0x22, 2)
        return self._translate_pair(bs[1], bs[0])
    
    @property
    def AQI(self) -> int:
        """
        Reads the calculated Air Quality Index (AQI) according to the UBA
        1 = Excellent
        2 = Good
        3 = Moderate
        4 = Poor
        5 = Unhealthy
        """
        return self.i2c.readfrom_mem(self.address, 0x21, 1)[0]
    
    def reset(self) -> None:
        """Resets and returns to standard operating mode (2)"""

        self.operating_mode = 0xF0 # reset
        time.sleep(1.0)
        self.operating_mode = 1
        time.sleep(0.25)
        self.i2c.writeto_mem(self.address, 0x12, bytes([0x00]))
        time.sleep(0.15)
        self.i2c.writeto_mem(self.address, 0x12, bytes([0xCC])) # reset command register
        time.sleep(0.35)
        self.operating_mode = 2
        time.sleep(0.50)



    
        
    def _translate_pair(self, high:int, low:int) -> int:
        """Converts a byte pair to a usable value. Borrowed from https://github.com/m-rtijn/mpu6050/blob/0626053a5e1182f4951b78b8326691a9223a5f7d/mpu6050/mpu6050.py#L76C39-L76C39."""
        value = (high << 8) + low
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value   
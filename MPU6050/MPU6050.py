"""
A lightweight MicroPython implementation for interfacing with an MPU-6050 via I2C. 
Author: Tim Hanewich - https://github.com/TimHanewich
Version: 1.0
Get updates to this code file here: https://github.com/TimHanewich/MicroPython-Collection/blob/master/MPU6050/MPU6050.py

License: MIT License
Copyright 2023 Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import machine

class MPU6050:
    """Class for reading gyro rates and acceleration data from an MPU-6050 module via I2C."""
    
    def __init__(self, i2c:machine.I2C, address:int = 0x68):
        """
        Creates a new MPU6050 class for reading gyro rates and acceleration data.
        :param i2c: A setup I2C module of the machine module.
        :param address: The I2C address of the MPU-6050 you are using (0x68 is the default).
        """
        self.address = address
        self.i2c = i2c
        
    def wake(self) -> None:
        """Wake up the MPU-6050."""
        self.i2c.writeto_mem(self.address, 0x6B, bytes([0x01]))

    def sleep(self) -> None:
        """Places MPU-6050 in sleep mode (low power consumption). Stops the internal reading of new data. Any calls to get gyro or accel data while in sleep mode will remain unchanged - the data is not being updated internally within the MPU-6050!"""
        self.i2c.writeto_mem(self.address, 0x6B, bytes([0x40]))
        
    def who_am_i(self) -> int:
        """Returns the address of the MPU-6050 (ensure it is working)."""
        return self.i2c.readfrom_mem(self.address, 0x75, 1)[0]
    
    def read_temperature(self) -> float:
        """Reads the temperature, in celsius, of the onboard temperature sensor of the MPU-6050."""
        data = self.i2c.readfrom_mem(self.address, 0x41, 2)
        raw_temp:float = self._translate_pair(data[0], data[1])
        temp:float = (raw_temp / 340.0) + 36.53
        return temp

    def read_gyro_range(self) -> int:
        """Reads the gyroscope range setting."""
        return self._hex_to_index(self.i2c.readfrom_mem(self.address, 0x1B, 1)[0])
        
    def write_gyro_range(self, range:int) -> None:
        """Sets the gyroscope range setting."""
        self.i2c.writeto_mem(self.address, 0x1B, bytes([self._index_to_hex(range)]))
        
    def read_gyro_data(self) -> tuple[float, float, float]:
        """Read the gyroscope data, in a (x, y, z) tuple."""
        
        # set the modified based on the gyro range (need to divide to calculate)
        gr:int = self.read_gyro_range()
        modifier:float = None
        if gr == 0:
            modifier = 131.0
        elif gr == 1:
            modifier = 65.5
        elif gr == 2:
            modifier = 32.8
        elif gr == 3:
            modifier = 16.4
            
        # read data
        data = self.i2c.readfrom_mem(self.address, 0x43, 6) # read 6 bytes (gyro data)
        x:float = (self._translate_pair(data[0], data[1])) / modifier
        y:float = (self._translate_pair(data[2], data[3])) / modifier
        z:float = (self._translate_pair(data[4], data[5])) / modifier
        
        return (x, y, z)
                
    def read_accel_range(self) -> int:
        """Reads the accelerometer range setting."""
        return self._hex_to_index(self.i2c.readfrom_mem(self.address, 0x1C, 1)[0])
    
    def write_accel_range(self, range:int) -> None:
        """Sets the gyro accelerometer setting."""
        self.i2c.writeto_mem(self.address, 0x1C, bytes([self._index_to_hex(range)]))
        
    def read_accel_data(self) -> tuple[float, float, float]:
        """Read the accelerometer data, in a (x, y, z) tuple."""
        
        # set the modified based on the gyro range (need to divide to calculate)
        ar:int = self.read_accel_range()
        modifier:float = None
        if ar == 0:
            modifier = 16384.0
        elif ar == 1:
            modifier = 8192.0
        elif ar == 2:
            modifier = 4096.0
        elif ar == 3:
            modifier = 2048.0
            
        # read data
        data = self.i2c.readfrom_mem(self.address, 0x3B, 6) # read 6 bytes (accel data)
        x:float = (self._translate_pair(data[0], data[1])) / modifier
        y:float = (self._translate_pair(data[2], data[3])) / modifier
        z:float = (self._translate_pair(data[4], data[5])) / modifier
        
        return (x, y, z)
        
    def read_lpf_range(self) -> int:
        return self.i2c.readfrom_mem(self.address, 0x1A, 1)[0]
    
    def write_lpf_range(self, range:int) -> None:
        """
        Sets low pass filter range.
        :param range: Low pass range setting, 0-6. 0 = minimum filter, 6 = maximum filter.
        """

        # check range
        if range < 0 or range > 6:
            raise Exception("Range '" + str(range) + "' is not a valid low pass filter setting.")
        
        self.i2c.writeto_mem(self.address, 0x1A, bytes([range]))

            
    #### UTILITY FUNCTIONS BELOW ####
        
    def _translate_pair(self, high:int, low:int) -> int:
        """Converts a byte pair to a usable value. Borrowed from https://github.com/m-rtijn/mpu6050/blob/0626053a5e1182f4951b78b8326691a9223a5f7d/mpu6050/mpu6050.py#L76C39-L76C39."""
        value = (high << 8) + low
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value   

    def _hex_to_index(self, range:int) -> int:
        """Converts a hexadecimal range setting to an integer (index), 0-3. This is used for both the gyroscope and accelerometer ranges."""
        if range== 0x00:
            return 0
        elif range == 0x08:
            return 1
        elif range == 0x10:
            return 2
        elif range == 0x18:
            return 3
        else:
            raise Exception("Found unknown gyro range setting '" + str(range) + "'")
        
    def _index_to_hex(self, index:int) -> int:
        """Converts an index integer (0-3) to a hexadecimal range setting. This is used for both the gyroscope and accelerometer ranges."""
        if index == 0:
            return 0x00
        elif index == 1:
            return 0x08
        elif index == 2:
            return 0x10
        elif index == 3:
            return 0x18
        else:
            raise Exception("Range index '" + index + "' invalid. Must be 0-3.")
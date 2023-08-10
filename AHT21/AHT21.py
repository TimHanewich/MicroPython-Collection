import machine
import time

class AHT21:
    """
    Lightweight class for communicating with an AHT21 temperature and humidity sensor via I2C.
    
    AHT21 Datasheet:
    http://www.aosong.com/userfiles/files/media/AHT21%20%E8%8B%B1%E6%96%87%E7%89%88%E8%AF%B4%E6%98%8E%E4%B9%A6%20A0%202020-12-8.pdf
    
    Code inspired by:
    https://github.com/any-sliv/aht21_python_pigpio/blob/main/aht21.py
    https://github.com/Thinary/AHT_Sensor/blob/main/AHT_Sensor/src/Thinary_AHT_Sensor.cpp
    """
    
    def __init__(self, i2c:machine.I2C, address = 0x38):
        """
        Creates a new instance of the AHT21 class
        :param i2c: Setup machine.I2C interface
        :param address: The I2C address of the AHT21 slave device
        """
        self.i2c = i2c
        self.address = address
        self.initialize()
        
    def initialize(self) -> None:
        """Initializes (calibrates) the AHT21 sensor"""
        self.i2c.writeto(self.address, bytes([0xbe, 0x08, 0x00]))
        time.sleep(0.1)
        self.i2c.writeto(self.address, bytes([0x71]))
        init_check = self.i2c.readfrom(self.address, 1)
        if not init_check[0] & 0x68 == 0x08:
            raise Exception ("Initialization of AHT21 failed!")
    
    def read(self) -> tuple[float, float]:
        """Reads the relative humidity (as a percentage) and temperature (in degrees celsius) as a tuple, in that order."""
        self.i2c.writeto(self.address, bytes([0xac, 0x33, 0x00]))
        time.sleep(0.2)
        res = self.i2c.readfrom(self.address, 6)
        
        # Relative humidity, as a percentage
        rh = ((res[1] << 16) | (res[2] << 8) | res[3]) >> 4;
        rh = (rh * 100) / 1048576

        # Temperature, in celsius
        temp = ((res[3] & 0x0F) << 16) | (res[4] << 8) | res[5];
        temp = ((200 * temp) / 1048576) - 50
        
        return (rh, temp)
    
import machine

class ENS160:
    """
    Lightweight class for communicating with an ENS160 air quality sensor via I2C.
    Follows the specifications defined in the official ENS160 data sheet: https://www.mouser.com/datasheet/2/1081/SC_001224_DS_1_ENS160_Datasheet_Rev_0_95-2258311.pdf
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
        if value not in [0, 1, 2]:
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
    
        
    def _translate_pair(self, high:int, low:int) -> int:
        """Converts a byte pair to a usable value. Borrowed from https://github.com/m-rtijn/mpu6050/blob/0626053a5e1182f4951b78b8326691a9223a5f7d/mpu6050/mpu6050.py#L76C39-L76C39."""
        value = (high << 8) + low
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value   
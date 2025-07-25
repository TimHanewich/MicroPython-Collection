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
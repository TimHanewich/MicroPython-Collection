import machine
import bmp085
import time

i2c = machine.I2C(0, sda=machine.Pin(16), scl = machine.Pin(17))
print(i2c.scan()) # should print 119 (0x77), the address of the BMP180

bmp = bmp085.BMP180(i2c)

# set barometric pressure at sea level for your area, measured in millibar.
# for example, Sarasota, Florida area is ~1016 mb (https://forecast.weather.gov/data/obhistory/KSRQ.html)
bmp.sealevel = 1016.0

# by default, the class is set to poll the pressure data 4 times each time you ask it for data, to get a better reading (oversample of 3)
# but, you can set the "oversample" to 0, 1, 2, or 3 to make it quicker, but less accurate.
bmp.oversample = 3

while True:
    tempc:float = bmp.temperature
    pressure = bmp.pressure
    altitude:float = bmp.altitude
    print("Temperature: " + str(tempc) + " °C, Pressure: " + str(pressure) + " hPa, Altitude: " + str(altitude) + " meters")
    time.sleep(1.0)
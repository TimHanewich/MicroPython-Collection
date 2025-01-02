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

# establish baseline altitude (where the drone 'started')
baseline:float = 0.0
for i in range(0, 5):
    print("Gathering baseline reading # " + str(i+1) + "... ")
    baseline = baseline + bmp.altitude
    time.sleep(1.0)
baseline = baseline / 5 # divide by 5 samples to get avg
print("Baseline altitutde: " + str(baseline) + " meters")

diff_meters:float = 0.0
while True:
    altitude:float = bmp.altitude
    diff_meters:float = (diff_meters * 0.9) + ((altitude - baseline) * 0.1) # pass through smoothing filter
    diff_centimeters = diff_meters * 100
    print("Relative altitude from starting point: " + str(round(diff_centimeters, 0)) + " cm")
    time.sleep(0.5)
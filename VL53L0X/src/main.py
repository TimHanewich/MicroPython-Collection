import time
import vl53l0x
import machine

i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
print(i2c.scan())

tof = vl53l0x.VL53L0X(i2c)

while True:
    distance:int = tof.ping() - 50 # subtract 50 to account for error (it always estimates 50 over!)
    if distance == 8140:
        print("Distance: out of range (beyond ~1200mm)")
    else:
        print("Distance: " + str(distance) + " mm")
    time.sleep(0.25)
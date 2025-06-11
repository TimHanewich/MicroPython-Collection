import time
import machine
import vl53l0x

# I2C that the multiplexer is attached to
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

# switch to channel 0 and then create tof sensor object
i2c.writeto(0x70, bytes([1 << 0]))
tof0 = vl53l0x.VL53L0X(i2c)

# switch to channel 1 and then create tof sensor object
i2c.writeto(0x70, bytes([1 << 1]))
tof1 = vl53l0x.VL53L0X(i2c)

while True:
    
    # capture sensor 0 reading
    i2c.writeto(0x70, bytes([1 << 0])) # switch to channel 0
    distance_sensor0 = tof0.ping() - 50
    
    # capture sensor 1 reading
    i2c.writeto(0x70, bytes([1 << 1])) # switch to channel 1
    distance_sensor1 = tof1.ping() - 50
    
    print("S1: " + str(distance_sensor0) + " mm, S2: " + str(distance_sensor1) + " mm")
    time.sleep(0.1)
import ENS160
import machine
import ENS160
import time

i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16), freq=100000)
print(i2c.scan())
sensor = ENS160.ENS160(i2c)

def loop():
    while True:
        print("At ticks " + str(time.ticks_ms()))
        print(str(sensor))
        print("----------------")
        time.sleep(1)
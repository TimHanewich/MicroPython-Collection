import ENS160
import machine
import ENS160
import time

i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16), freq=100000)
print(i2c.scan())
sensor = ENS160.ENS160(i2c)

def loop():
    while True:
        print("AQI: " + str(sensor.AQI))
        print("TVOC: " + str(sensor.TVOC))
        print("ECO2: " + str(sensor.ECO2))
        print("Error: " + str(sensor.error))
        print("New Data Available: " + str(sensor.new_data_available))
        print("Signal rating: " + str(sensor.signal_rating))
        print("------------------")
        time.sleep(1)
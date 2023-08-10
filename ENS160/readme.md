

## Example Usage
```
i2c = machine.I2C(0, sda=machine.Pin(12), scl=machine.Pin(13))
ens = ENS160(i2c)
ens.operating_mode = 2 # turn on reading mode (awaken from sleep)
print(ens.CO2) # 559
print(ens.TVOC) # 106
print(ens.AQI) # 2
```
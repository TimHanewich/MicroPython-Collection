## Example Usage
```
i2c = machine.I2C(0, sda=machine.Pin(12), scl=machine.Pin(13))
aht = AHT21(i2c)
print(aht.read()) # (40.24334, 30.33524)
```
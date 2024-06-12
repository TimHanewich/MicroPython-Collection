# ENS160.py
A lightweight class for interfacing with an ENS160 digital multi-gas sensor. This class was built to interface with the ENS160 according to [it's official datasheet](https://github.com/TimHanewich/MicroPython-Collection/releases/download/1/ENS160_datasheet.pdf).

## Example Usage
```
i2c = machine.I2C(0, sda=machine.Pin(12), scl=machine.Pin(13))
ens = ENS160(i2c)
ens.operating_mode = 2 # turn on reading mode (awaken from sleep)
print(ens.AQI) # {'value': 2, 'text': 'good'}
print(ens.TVOC) # 106
print(ens.ECO2) # 559
```

I also provided an example script [here](./example.py). However, please note this does not include recommended built-in logic for how to handle a scenario in which the ENS160 stops functioning randomly (read on below).

## Poor Reliability Issues
I have had much success with the SparkFun ENS160 I bought [on Amazon](https://a.co/d/i8LiwVQ). However, some forms of the ENS160 sensor, like [these ones I purchased on Amazon](https://a.co/d/id3JsgZ), I have found are very unreliable. I've tried many things to get them to return stable readings, with no success. My trials are documented [in this repo](https://github.com/TimHanewich/diagnosing-ens160).
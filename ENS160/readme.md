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
I purchased ENS160 + AHT21 sensors on a single breakout board from Amazon [here](https://a.co/d/id3JsgZ). I am not sure if this issue is specific to this item I purchased, but I have been experiencing serious reliability issues with the ENS160. Oftentimes, the ENS160 will work perfectly for anywhere between one minute and 30 minutes. And then, suddenly, it just starts returning invalid data. All values (AQI, TVOC, ECO2) are "0". And there isn't any particular error or problem indicated by the sensor.

I've been struggling to figure out the root issue of this, without success. I documented some of these struggled in [this repository](https://github.com/TimHanewich/diagnosing-ens160). For whatever reason, I have not been able to replicate these problems with the sensor on a "standard" Raspberry Pi (the ones that pack a full Linux operating system). I only seem to encounter these reliability problems when interfacing with the ENS160 through a Raspberry Pi Pico.

After much testing, it seems to be unavoidable. I really do not think I am doing anything wrong to the sensor (i.e. writing an invalid value to a register) that is causing this. I am not sure why, but after some period of time functioning, the sensor just steps reading.

Fortunately, it seems that a fix is reasonably simple: in your code, add some logic that checks if the output is valid. And if it isn't valid, "reboot" the sensor simply by setting the `operating_mode` equal to `2` (standard gas sensing mode). Wait 10 seconds, and then proceed to read values. From my experience, this has gotten the sensor to come back to life and work again, returning reliable data... at least for some time until it does it again!

You can find examples of this in both [this file (uses a helper class)](https://github.com/TimHanewich/diagnosing-ens160/blob/master/src/pico/test2/test.py) and [this file (raw I2C communication)](https://github.com/TimHanewich/diagnosing-ens160/blob/master/src/pico/test1/test.py) as well as the results these tests documented [here](https://github.com/TimHanewich/diagnosing-ens160/tree/master/src/pico).
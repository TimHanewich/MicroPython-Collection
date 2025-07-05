# Using the GUVA-S12SD Solar UV Intensity Sensor
Ultraviolet (UV) rays are a form of electromagnetic radiation emitted by the sun, with wavelengths shorter than visible light but longer than X-rays. While essential for processes like vitamin D synthesis, excessive exposure to UV rays, especially UVB, can pose serious health risks, including skin cancer, cataracts, and premature aging. 

The GUVA-S12SD sensor offers a practical way to monitor UV intensity by detecting light in the 240–370 nm range, which covers most of the UVA and UVB spectrum. It outputs an analog voltage proportional to the UV light it receives, allowing users to estimate the UV index and assess potential exposure levels. This makes it a valuable tool for DIY weather stations, wearable sun safety devices, and environmental monitoring projects.

![sensor](https://i.imgur.com/b4UwUjA.jpeg)

I purchased [these GUVA-S12SD sensors](https://a.co/d/jarZjR8) from Amazon and had success with them!

## Wiring
The GUVA-S12SD only has three pins: **VCC**, **GND**, and **SIG**. 
- Connect **VCC** to the Pi's 3.3v supply
- Connect **GND** to any of the Pi's ground pins
- Connect **SIG** to one of the Pi's analog-to-digital converter pins (I use GP26 usually)

I've seen some tutorials (and product descriptions) say you can connect it to a 5V or 3.3V supply - that is true! However, the *output voltage* of the sensor will differ base on the input VCC voltage. If you connect it to a 5V power source, its *max* reading will be close to 5V, well outside of the Pi's 3.3V range, possibly damaging it. So, I've found 3.3V to work perfectly!

## Example Code
Use [GUVA_S12SD.py](./GUVA_S12SD.py), a MicroPython module with a driver for the GUVA-S12SD to read the UV index. An example on how to use the driver is shown below:

```
import machine
import GUVA_S12SD
import time

# set up GUVA
guva = GUVA_S12SD.GUVA_S12SD(26) # ADC on GP26

while True:
    uvi:int = guva.UVI # read the UV Index
    print("UVI: " + str(uvi))
    time.sleep(0.25)
```

## How it Works
The GUVA-S12SD is actually a quite simple sensor! It is an analog sensor, which means it simply outputs a voltage reading on its signal pin that indicates how much UV light it is getting at any given moment - as the UV light increases, the voltage rises; as the UV light decreases, the voltage decreases.

Using a MicroController like the Raspberry Pi Pico, we can read this voltage level that the sensor outputs on its SIG (signal) pin to infer the UV Index. I won't go into detail about how this is done here, but it is quite simple, just check out [the code in the driver](./GUVA_S12SD.py)!

Anyway, once we calculate the voltage that the sensor is transmitting over its SIG pin, we can use this handy graph that the manufacturer provides to convert from voltage (expressed here as *mV*) to the UV Index:

![mV to UV Index](https://i.imgur.com/qtNq3Wm.png)

*Note, the graph is quite confusing... It is noted that UV index of 0 has a mV less than 50, and then a UV index of 1 begins at 227 mV... so what is the UV index between 50 mV and 227 mV? In my case, I simply assumed that window is also a UV index of 0!*
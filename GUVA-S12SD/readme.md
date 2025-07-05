# Using the GUVA-S12SD Solar UV Intensity Sensor
Ultraviolet (UV) rays are a form of electromagnetic radiation emitted by the sun, with wavelengths shorter than visible light but longer than X-rays. While essential for processes like vitamin D synthesis, excessive exposure to UV rays, especially UVB, can pose serious health risks, including skin cancer, cataracts, and premature aging. 

The GUVA-S12SD sensor offers a practical way to monitor UV intensity by detecting light in the 240–370 nm range, which covers most of the UVA and UVB spectrum. It outputs an analog voltage proportional to the UV light it receives, allowing users to estimate the UV index and assess potential exposure levels. This makes it a valuable tool for DIY weather stations, wearable sun safety devices, and environmental monitoring projects.

I purchased [these GUVA-S12SD sensors](https://a.co/d/jarZjR8) from Amazon and had success with them!

## Wiring
The GUVA-S12SD only has three pins: **VCC**, **GND**, and **SIG**. 
- Connect VCC to the Pi's 3.3v supply
- Connect GND to any of the Pi's ground pins
- Connect SIG to one of the Pi's analog-to-digital converter pins (I use GP26 usually)

I've seen some tutorials (and product descriptions) say you can connect it to a 5V or 3.3V supply - that is true! However, the *output voltage* of the sensor will differ base on the input VCC voltage. If you connect it to a 5V power source, its *max* reading will be close to 5V, well outside of the Pi's 3.3V range, possibly damaging it. So, I've found 3.3V to work perfectly!

## Example Code

## How it Works
![mV to UV Index](https://i.imgur.com/qtNq3Wm.png)
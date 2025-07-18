# MicroPython Driver for the AHT Sensor Series
The AHT series of temperature and humidity sensors, developed by Aosong Electronics, are compact, digital-output environmental sensors designed for precision and ease of integration. These sensors communicate over I²C using a fixed address (0x38) and a simple command set, making them ideal for embedded systems and IoT applications.

Models like the AHT10, AHT20, and AHT21 offer factory-calibrated measurements with typical accuracies of ±0.3 °C for temperature and ±2% RH for humidity. They feature low power consumption, fast response times, and wide operating ranges, with the AHT21 extending temperature support up to 120 °C for industrial and medical use.

Thanks to their shared protocol and register map, these sensors are interchangeable in software, allowing developers to write unified drivers that support multiple AHT variants with minimal effort.

## AHT-Series Overview
| Sensor   | Temp Range (°C) | Humidity Range (%RH) | Temp Accuracy | Humidity Accuracy | Package Height | Power Supply | Common Applications |
|----------|------------------|------------------------|----------------|--------------------|----------------|---------------|----------------------|
| **AHT10** | -40 to +85       | 0 to 100               | ±0.3 °C        | ±2% RH             | ~1.0 mm        | 2.0–5.5V      | Home automation, weather stations, HVAC |
| **AHT15** | -40 to +85       | 0 to 100               | ±0.3 °C        | ±2% RH             | ~1.0 mm        | 2.0–5.5V      | Similar to AHT10, less common |
| **AHT20** | -40 to +85       | 0 to 100               | ±0.3 °C        | ±2% RH             | 1.0 mm         | 2.0–5.5V      | IoT, industrial monitoring, consumer electronics |
| **AHT21** | -40 to +120      | 0 to 100               | ±0.3 °C        | ±2% RH             | 0.8 mm         | 2.0–5.5V      | Medical devices, harsh environments, smart agriculture |
| **AHT25** | -40 to +125      | 0 to 100               | ±0.1 °C        | ±1.8% RH           | ~0.8 mm        | 2.0–5.5V      | High-precision industrial and scientific use |

If you are looking to purchase sensors, I purchased [these](https://a.co/d/9wQiXdT) and had success with them. As one of the reviews noted, I noticed the temperature reading is a tad higher than a DHT-22 I had sitting in close proximity to it. The difference in my tests was ranged from ~0.6-0.8 degrees Fahrenheit.

## Example Usage
The driver provided ([aht.py](./aht.py)) should work with any AHT sensor in the entire series because all sensors follow the identical I2C communication protocol (same address, registers, commands, etc).

Below is an example of using the driver:

```
from machine import I2C
from aht import AHTXX
import time

i2c = I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
print(i2c.scan()) # 56, or "0x38" is the standard address for any AHT sensor

# sensor initialization
sensor = AHTXX(i2c)
sensor.initialize() # wakes up the sensor, calibrate, gets it ready
time.sleep(0.5)

while True:
    data = sensor.read()
    print("Relative Humidity: " + str(round(data[0], 1)) + "%")
    print("Temperature: " + str(round(data[1], 1)) + " C")
    time.sleep(1.0)
```

As seen above, you can use the `read()` function to read both the relative humidity and temperature data (it comes as a single packet). The relative humidity is always the first value in the tuple while temperature (in celcius) is always second.
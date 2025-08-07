# MicroPython Driver for the TF Luna (I2C Mode)
The TF-Luna is a compact, low-cost single-point LiDAR range sensor developed by Benewake. It's designed for accurate distance measurement using the Time-of-Flight (ToF) principle, which calculates distance by measuring the time it takes for infrared light to bounce off a target and return to the sensor.

The TF Luna can operate (provide data) via UART or by I2C. The driver I provide here is designed for I2C mode.

DroneBot Workshop made a wonderful video about the TF Luna, found [here](https://www.youtube.com/watch?v=SJCnLY4onWc).

## Booting in I2C Mode
![pinout](https://i.imgur.com/cJzmlyu.png)

Note that in order to be in I2C mode, you need to have Pin 5 pulled to ground (connected to GND) **when the TF Luna boots** (when it is provided power). Booting it first *and then* connecting Pin 5 to ground will not put it in I2C mode.

## No Driver Example
The snippet of code below demonstrates reading from the TF Luna without any driver at all, if that is what you are looking to do. Just a simple script to read from the I2C registers, convert it to an int16, and display it.

```
import machine
import time

i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))

while True:
    distance_bytes:bytes = i2c.readfrom_mem(0x10, 0x00, 2)
    distance:int = distance_bytes[1] << 8 | distance_bytes[0]
    print(str(distance) + " cm")
    time.sleep(0.25)
```

## Documentation
Benewake, the maker of the TF Luna, provides great documentation.

The TF-Luna user manual can be found [here](https://en.benewake.com/uploadfiles/2024/04/20240426135946148.pdf).

The I2C register table can be found on page 36, included below as well:

![register_table_1](https://i.imgur.com/BZDxhdT.png)

![register_table_2](https://i.imgur.com/E7PpwZG.png)
# MicroPython Driver for the QMC5883L Magnetometer
This repository contains a custom Python driver for the **QMC5883L** three-axis digital magnetometer, designed for seamless integration with microcontrollers, drones, robotics platforms, and embedded systems. The driver supports I²C communication and automatic offset calibration.

Built with clarity and extendability in mind, the code provides low-level access to raw magnetic field readings along with high-level calibration routines. Whether you're building a drone, a mobile robot, or an educational compass project, this driver gives you full control over your sensor pipeline without relying on bulky external libraries.

## What is the QMC5883L?
The **QMC5883L** is a compact, high-performance digital magnetometer capable of measuring magnetic fields across three axes. It's widely used in navigation systems to determine orientation based on the Earth's magnetic field.

Internally, it uses **anisotropic magneto-resistive (AMR) sensors** and features:
- A 16-bit ADC for high resolution
- Built-in temperature compensation
- Automatic magnetic offset cancellation
- I²C communication interface

Its low power consumption and small footprint make it ideal for embedded applications such as drones, robotic rovers, and electronic compasses.

## Wiring
|QMC5883L Pin|MicroController Pin|
|-|-|
|VCC|+ 3.3V|
|GND|GND|
|SDA|Any I2C SDA pin (i.e. GP16 on the Raspberry Pi Pico)|
|SCL|Any I2C SCL pin (i.e. GP17 on the Raspberry Pi Pico)|

## Basic Use Demo
Basic use demonstration, reading the raw X, Y, and Z magnetometer values:
```
import machine
import time
from QMC5883L import QMC5883L

i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
print(i2c.scan()) # [13]
qmc = QMC5883L(i2c)

while True:
    print(qmc.read())
    time.sleep(0.5)
```

Note that the script above will only output the raw X, Y, and Z values from the magnetometer. On their own, these aren't very helpful. So, continue reading on below to learn how we can also get **the absolute heading**!

## How to use the QMC5883L as a Compass
The most common use of the QMC5883L is as a compass. The raw magnetometer values from the QMC5883L can be transformed into an approximate heading (in degrees), between 0 and 360. But, to do that, there are a few steps we have to take.

### Step 1: Calibration
The first step is *calibration*. But don't let this scare you! This is nothing more than flipping the QMC5883L around and observing the **minimum** and **maximum** observed values on all three axes. After observing these, we can provide these to the `QMC5883L` class for them to be used to "center" (offset correction) the incoming raw magnetometer values.

The following is a simple calibration script that you can run on your MicroController to get the min and max values:

```
# CALIBRATION SCRIPT

import machine
import time
from QMC5883L import QMC5883L

i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
print(i2c.scan()) # [13]
qmc = QMC5883L(i2c)

started_at = time.ticks_ms()
min_x:int = 999999
max_x:int = 0
min_y:int = 999999
max_y:int = 0
min_z:int = 999999
max_z:int = 0
while (time.ticks_ms() - started_at) < 10000:
    x, y, z = qmc.read()
    min_x = min(x, min_x)
    max_x = max(x, max_x)
    min_y = min(y, min_y)
    max_y = max(y, max_y)
    min_z = min(z, min_z)
    max_z = max(z, max_z)
    time.sleep(0.1)
    print("Calibrating...")
    
print("X: " + str(min_x) + " to " + str(max_x))
print("Y: " + str(min_y) + " to " + str(max_y))
print("Z: " + str(min_z) + " to " + str(max_z))
```

The script above observes the X, Y, and Z readings for 10 seconds as you move it around before printing out the min and max values for each axis.

### Step 2: Provide These Extrema to the QMC5883L Class
Now that we know each axis' extrema, we can provide these to the QMC5883L class:

```
# Calibrate QMC5883L by providing the extrema observed on all 3 axes
# input order: x_min, x_max, y_min, y_max, z_min, z_max
qmc.calibrate(1166, 1942, 1076, 1647, 2788, 2951)
```

### Step 3: Read the Heading!
With those extrema provided, we can now accurately calculate the heading!

```
import machine
import time
from QMC5883L import QMC5883L

# set up QMC5883L
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
print(i2c.scan()) # [13]
qmc = QMC5883L(i2c)

# Calibrate QMC5883L by providing the extrema observed on all 3 axes
# input order: x_min, x_max, y_min, y_max, z_min, z_max
qmc.calibrate(1166, 1942, 1076, 1647, 2788, 2951)

while True:
    print("Heading: " + str(qmc.heading) + " degrees")
    time.sleep(0.1)
```
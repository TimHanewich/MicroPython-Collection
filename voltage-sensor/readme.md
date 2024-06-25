# Voltage Sensor
I purchased [this voltage detection sensor](https://www.amazon.com/gp/product/B07L81QJ75/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1) on Amazon and have developed a module in MicroPython for reading analog values from it and converting this into a voltage reading. This class was designed and tested on the Raspberry Pi Pico (RP2040), but could be used on other hardware.

![what i bought](https://i.imgur.com/w0DztuT.png)

As noted in the description, on 3.3V systems (the Raspberry Pi Pico I am using), the maximum detected voltage is 16.5; in reality, I tested it to be around 16.3. I don't believe this means it will *damage* the sensor or other hardware in anyway, I believe this only means that it will not be able to tell if the voltage goes over this voltage level. So, in my `VoltageSensor` class described below, the returned value of the `voltage` function will not surpass the 16.3 I tested against and had the most success with.

**Check out [this video](https://youtube.com/shorts/fh43cqcYhMk) of it in action!**

## Wiring
- VCC and GND input from battery serves as input into the module
- "-" Pin to GND on Raspberry Pi Pico. I used pin 38.
- "S" Pin to one of the Analog-Digital-Conversion (ADC) pins on the Raspberry Pi Pico. I used pin 38 (GPIO 28) on the Raspberry Pi Pico.

## Example Usage
```
import voltage
import time
vs = voltage.VoltageSensor(28)
while True:
	print(round(vs.voltage(), 1))
```

The above script will continuously take voltage readings and print them.

## Development Notes
During development, I took a series of measurements with varying voltage inputs to the sensor module and observed the Raspberry Pi Pico's (RP2040) U16 ADC reading. That is included below:

![readings](https://i.imgur.com/jVJOcZT.png)

You can see in the chart above that the relationship between the voltage and analog reading is linear. This understanding is what the `voltage` function of the `VoltageSensor` module is based on.

## Measuring the Voltage of its own Power Source
I performed some testing on June 25, 2024. For whatever reason, the voltage measured is consistently *lower* than it actually is by sometimes up to a full volt, sometimes more.

Through multiple tests, I narrowed this down to this problem arising specifically when a Raspberry Pi Pico is measuring the voltage of a battery that is also powering the Pico itself. During my tests, I was using an MT3608 voltage converter to lift the voltage of the battery to a stable 5V.

Even when not using the MT3608 converted, when powering directly from solid 5V provided by DC-DC power supply, still had issue. It couldn't sense the 5V correctly. Was reading around 3.8 or 3.9

Still on a 5V supply from DC power, I then had it instead sense the voltage of an 18650 battery. Not a battery being used in any way, just the voltage of a standalone battery. Still incorrect.
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

### Tests I've run
- Seems to work: Configuration 1, running [test1](./test1/)
	- Powering pico via 5V from DC-DC.
	- Voltage sensor is also powered via 5V DC-DC
	- Voltage sensor hooked up to battery under no load (just sitting).
- Seems to work: Configuration 2, running [test1](./test1/)
	- Powering pico from MT3608 boosted to 5V. 
	- M3608 supplied power via 18650 battery.
	- Voltage sensor plugged into 18650 battery
	- Voltage sensor powered from MT3608 boosted 5V (along with the pico)
- Seeing problems: Running [test2](./test2/) in the same configuration as configuration 2:
	- Real voltage of battery (multimeter): 4.05v
	- Read voltage on screen, with neopixel attached and working: 3.88v
	- When I re-booted without the neopixel attached: 3.98v
		- As soon as I plug the neopixel back in and they are working, the voltage drops to 3.88v again.
- [test3](./test3/) - this test is to observe the ambient noise (value) on the ADC GP pin 26 when powered by USB or external.
	- On USB: `12,000`
	- On external: `10,300`
	- This is just due to noise. No need to worry about these differences I do not think.

## Tests I've run after realizing my wiring may have been wrong the night of June 25, 2024
In the wiring diagram on Amazon, they do not have a +5V being connected. I was connecting it. Maybe providing the voltage sensor with its own power through things off. I don't know.
- [test4](./test4/) - same as [test1](./test1/) but no SSD-1306 display. Just printing over REPL for now (want to see if SSD-1306 has any effect)
	- When plugged in via USB, reading from a battery under no load, this seems to work very well.
	- I am noticing long-term noise patterns. Where it will read 4.05v (correct) for a period of time, and then 20 seconds later creep up to 4.12 and then 20 seconds later creep back down to 4.05, then creep down to 4.02. Weird.
		- I noticed this same behaviour when the pin is floating, not being used (in [test3](./test3/)). Perhaps it is this behaviour still penetrating through to these readings.
- Running [test1](./test1/) on USB power.
	- The pico is still being powered by USB
	- The battery is still under no load
	- The SSD-1306 is now wired in and being used.
	- https://i.imgur.com/fv3mjM6.jpeg
	- Again, works very well just as test4 does.
- [test5](./test5/)
	- It seems like this is a difference in ambient state noise being read on the ADC channels.
	- Test 5 reads all 3 of the pico's ADC channels and just displays them to the SSD-1306.
	- I want to run this code in the following configurations:
		- On USB power, nothing attached.
		- On battery power (using MT3608 boost to 5V is fine), nothing attached.
		- On USB power, voltage sensor attached, sensing external no-load battery.
		- On battery power, voltage sensor attached, sensing external no-load battery.
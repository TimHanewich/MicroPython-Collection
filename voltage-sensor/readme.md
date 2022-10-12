I purchased [this voltage detection sensor](https://www.amazon.com/gp/product/B07L81QJ75/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1) on Amazon and have developed a module in MicroPython for reading analog values from it and converting this into a voltage reading. This class was designed and tested on the Raspberry Pi Pico (RP2040), but could be used on other hardware.

## Wiring
- VCC and GND input from battery serves as input into the module
- "+" Pin to 5V source. I used VBUS (pin 40) on Raspberry Pi Pico
- "-" Pin to GND on Raspberry Pi Pico. I used pin 38.
- "S" Pin to one of the Analog-Digital-Conversion (ADC) pins on the Raspberry Pi Pico. I used pin 38 (GPIO 28) on the Raspberry Pi Pico.

## Example Basic Reading
```
import voltage_sensor
import time

vs = voltage_sensor.voltage_sensor(28)

while True:
	volt_reading = vs.measure()
	print("Volts detected: " + str(volt_reading))
	time.sleep(0.25)
```

## Example Set Reading
The analog readings from the module are rather unstable and tend to "jump all over the place". Readings using the method above are quick, but could fluctuate as much as 0.2V over the course of a less than a second. To combat this, you can use the `measure_set` method to take a series of sample readings and then receive an average.
```
import voltage_sensor
import time

vs = voltage_sensor.voltage_sensor(28)

while True:
	volt_reading = vs.measure_set()
	print("Volts detected: " + str(volt_reading))
	time.sleep(0.25)
```
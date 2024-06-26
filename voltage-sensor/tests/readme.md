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
- [test5](./test5/) - **ignore these results, I think I was testing different batteries here**
	- It seems like this is a difference in ambient state noise being read on the ADC channels.
	- Test 5 reads all 3 of the pico's ADC channels and just displays them to the SSD-1306.
	- I want to run this code in the following configurations:
		- On USB power, nothing attached. **Result: random between 7,000 and 14,000**
		- On battery power (using MT3608 boost to 5V is fine), nothing attached. **Result: random, but seems to stick around 12,000**
		- On USB power, voltage sensor attached, sensing external no-load battery. **Result: large range of random values around 16,050, but all over the place. Still averages out stably probably**
		- On battery power, voltage sensor attached, sensing external no-load battery. **Result: Solid around 16,050**
		- On battery power, voltage sensor attached, sensing the voltage of its own battery. **Result: 16,800 it seems**
- [test6](./test6/)
	- I was worried I was only sampling the curve at the high/low end by change so I am going to burst sample now using the VoltageSensor class.
	- Want to conduct same tests as in [test5](./test5/)
		- On USB power, nothing attached. 
		- On battery power (using MT3608 boost to 5V is fine), nothing attached. 
		- On USB power, voltage sensor attached, sensing external no-load battery. **Result: Avg 13,400**
		- On battery power, voltage sensor attached, sensing external no-load battery. 
		- On battery power, voltage sensor attached, sensing the voltage of its own battery. **Result: Avg 13,300**
- [test7](./test7) - doing what [test6](./test6/) does, but print over REPL, not SSD1306
- [test8](./test8/) - same as [test6](./test6/), but with powering 12 neopixels w/ different random colors each cycle


## Seeing consistent readings
Using burst sampling from test 6, I've observed a stable hover around 13,350 for a battery @ 4.06v. And that is powering it via battery power through MT3608 boost.

When on USB power, I've observed the same results. Same analog values.

Also, when on USB power using REPL, observed same results. Same analog values.

I also tried to run [test7](./test7/) which continuously printed the results through REPL, not to the SSD-1306. Same results, same analog readings. Weird. 

Weird that it is working so well now. I also tried plugging in the +5V to VBUS while under USB power. Same results. It is behaving so well.

## Testing with battery under signifiant load vs. not
In [test8](./test8/), I had a strand of neopixels lighting up for 8 seconds and then turning off for 8 seconds. 

You could see the different in analog readings when they were on vs. off.
- Reading while the pixels were on: 11,900
- Reading while the pixels were off: 13,100

I also observed this on the multimeter, but differing by 0.02v. Not much.


## Observing Raw ADC Readings of Voltages applied to ADC
Using a voltage divider with equal resistors, a maximum of 4.2V (fully charged of 18650) would be split down to 2.1. And a minimum charge of 3.0V would be split down to 3.0 (50% in both scenarios, divided in half perfectly).

Here is the reading on the ADC pin of the Pico for both 1.5V (empty) and 2.1V (full):
- 1.5V: 30,500
- 2.1V: 42,700

In other words, it appears the raw reading on the ADC pin fluctuates by 20,333 per difference in 1.0 volt. Go up one volt, it should be about 20,333 points higher, go down one volt, it should be about 20,333 lower. Give or take. **But, that is on the split voltage**. So in reality, the difference in recognized voltage on the ADC channel needs to be multiplied by two to restore it to its full state (we split it in half via the voltage divider). 

... So, really, a difference in reading of 10,167 makes up a full volt difference on the battery. So, for example, being off in reading by 1,000 on the ADC channel would equate to only about 0.1 volts of a difference. Close enough.
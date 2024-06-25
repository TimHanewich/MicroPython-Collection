# Tim's MicroPython Collection
This repository contains a collection of reusable and protable MicroPython code. I've developed these modules for many of my Raspberry Pi Pico/Pico W projects and am hosting them in a centralized location here. 
None of these modules are in PyPi. If you wish to use any of them, copy and paste them into your project!

## In this Collection
- [Voltage Sensor](./voltage-sensor/) for reading battery voltages from [a voltage detection sensor terminal](https://www.amazon.com/gp/product/B07L81QJ75/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1).
- [BatteryMonitor.py](./BatteryMonitor/) - Simple class for translating a battery's voltage to a State-of-Charge percentage reading.
- [Color Toolkit](./color_toolkit/) - A toolkit for working with and manipulating RGB colors.
- [HCSR04](./HCSR04/) - Module for measuring distance with an HCSR04 ultrasonic range finder.
- [wlan_helper](./wlan_helper/) - a helper module for connecting to a WLAN (wifi) in MicroPython using the *network* module.
- [request_tools](./request_tools/) - Helper module for parsing an incoming HTTP request (received from a socket in a web server type scenario)
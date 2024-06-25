"""
Translates the analog signal from a Voltage Sensor to Volts
Author Tim Hanewich, github.com/TimHanewich
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/tree/master/voltage-sensor

MIT License
Copyright Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import machine
import time
       
class VoltageSensor:
    def __init__(self, adc_gpio:int) -> None:
        self._adc = machine.ADC(adc_gpio)

    def _sample_analog(self, duration:float = 0.5, samples:int = 10) -> int:
        """Takes average of analog reading over short period of time."""
        # I've learned that, no matter what duration you take samples over, the min, mean, and max should be the same. So taking these samples rapidly over 1.5 seconds is fine.
        delay:float = duration / samples
        total:int = 0
        for _ in range(samples):
            total = total + self._adc.read_u16()
            time.sleep(delay)
        return int(round(total / samples, 0))

    def voltage(self, duration:float = 0.5, samples:int = 10) -> float:
        """Burst-samples analog reading and converts to voltage estimate."""
        analog:int = self._sample_analog(duration, samples)
        max_analog:int = 65535
        min_analog:int = 600
        max_voltage:float = 16.3
        min_voltage:float = 0.0
        TR:float = ((analog - min_analog) / (max_analog - min_analog)) * (max_voltage - min_voltage)
        TR = min(max(TR, min_voltage), max_voltage)
        return TR
    
